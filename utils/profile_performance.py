import tracemalloc
import functools
import time


def profile_memory_and_time(func):
    """
    A decorator that profiles the memory usage and execution time of a function
    using tracemalloc.
    It measures the memory allocated by Python during the function's execution
    and the peak memory usage during that time. It aims to isolate the memory
    usage of the decorated function, excluding the baseline Python interpreter
    memory as much as possible.
    Args:
        func (callable): The function to be profiled.
    Returns:
        callable: A wrapper function that, when called, executes the original
                  function and returns a tuple:
                  (original_result, profile_info)
                  where 'profile_info' is a dictionary containing:
                  {
                      'result': The return value of the wrapped function.
                      'time_seconds': Execution time in seconds.
                      'memory_start_bytes': Traced memory before execution.
                      'memory_end_bytes': Traced memory after execution.
                      'memory_peak_bytes': Peak traced memory during execution.
                      'memory_allocated_diff_bytes': Net memory change (bytes)
                                                    between start and end snapshots.
                                                    Positive means more memory
                                                    allocated than freed.
                      'top_allocations': A list of dictionaries, detailing the
                                         top 5 sources of memory difference
                                         (allocations - deallocations) during
                                         the function call. Each dict contains:
                                         {'filename': str,
                                          'lineno': int,
                                          'size_diff_bytes': int,
                                          'count_diff': int}
                  }
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        was_tracing = tracemalloc.is_tracing()
        if not was_tracing:
            tracemalloc.start()

        # Clear previous traces and get memory before execution
        tracemalloc.clear_traces()
        mem_before = tracemalloc.get_traced_memory()[0]  # Current memory
        snapshot_before = tracemalloc.take_snapshot()
        start_time = time.perf_counter()

        # Execute the function
        result = func(*args, **kwargs)

        # Measure time and memory after execution
        end_time = time.perf_counter()
        mem_after, mem_peak = (
            tracemalloc.get_traced_memory()
        )  # Current and peak memory since clear_traces
        snapshot_after = tracemalloc.take_snapshot()

        if not was_tracing:
            # Stop tracing only if this wrapper started it
            tracemalloc.stop()

        # --- Process Results ---
        execution_time = end_time - start_time

        # Calculate difference between snapshots
        # Group by traceback to aggregate allocations from the same call stack
        stats = snapshot_after.compare_to(snapshot_before, "traceback")
        total_allocated_diff = sum(stat.size_diff for stat in stats)

        # Get details of top 5 differences
        top_stats_details = []
        # Limit grouping depth for readability if needed, e.g., key_type='lineno'
        # Using 'traceback' gives more context but can be verbose. Let's stick to lineno for top stats.
        stats_lineno = snapshot_after.compare_to(snapshot_before, "lineno")
        for stat in stats_lineno[:5]:  # Top 5 lines causing memory changes
            # Find the frame corresponding to the user's code if possible
            # The direct frame info is simpler here
            frame = stat.traceback[0]  # Get the first frame (most recent call site)
            top_stats_details.append(
                {
                    "filename": frame.filename,
                    "lineno": frame.lineno,
                    "size_diff_bytes": stat.size_diff,  # Net change for this line
                    "count_diff": stat.count_diff,  # Net change in block count
                }
            )

        profile_info = {
            "time_seconds": execution_time,
            "memory_start_bytes": mem_before,
            "memory_end_bytes": mem_after,
            "memory_peak_bytes": mem_peak,
            "memory_allocated_diff_bytes": total_allocated_diff,
            "top_allocations": top_stats_details,
        }

        # Return the original result separately as well, common pattern
        return result, profile_info

    return wrapper


# --- Example Usage ---


@profile_memory_and_time
def create_large_list(n):
    """Creates a list of n integers."""
    print(f"Creating a list with {n} elements...")
    # Deliberately less efficient string conversion to use more memory
    return [str(i) * 10 for i in range(n)]


@profile_memory_and_time
def process_data(data):
    """Processes the data by creating a new list of lengths."""
    print("Processing data...")
    # Force allocation of new list
    lengths = [len(s) for s in data]
    # Create another structure
    processed = {i: lengths[i] for i in range(len(lengths) // 2)}
    time.sleep(0.1)  # Simulate some work
    return len(processed)


if __name__ == "__main__":
    # Run the first function
    list_size = 100_000
    my_list, profile1 = create_large_list(list_size)
    print("\n--- Profile for create_large_list ---")
    print(f"Function Result: List length = {len(my_list)}")
    print(f"Execution Time: {profile1['time_seconds']:.4f} seconds")
    print(f"Memory Before (traced): {profile1['memory_start_bytes'] / 1024:.2f} KiB")
    print(f"Memory After (traced): {profile1['memory_end_bytes'] / 1024:.2f} KiB")
    print(f"Memory Peak (traced): {profile1['memory_peak_bytes'] / 1024:.2f} KiB")
    print(
        f"Net Memory Diff (traced): {profile1['memory_allocated_diff_bytes'] / 1024:.2f} KiB"
    )
    print("Top 5 Memory Allocation Differences:")
    for alloc_stat in profile1["top_allocations"]:
        print(
            f"  - File: {alloc_stat['filename']}, Line: {alloc_stat['lineno']}, "
            f"Size Diff: {alloc_stat['size_diff_bytes']} bytes, "
            f"Count Diff: {alloc_stat['count_diff']}"
        )

    print("\n" + "=" * 40 + "\n")

    # Run the second function using the result of the first
    processed_len, profile2 = process_data(my_list)
    # We don't need the large list anymore here in a real scenario
    # If we wanted to measure its deallocation, tracemalloc could show it
    # if garbage collection runs and tracing is still active.
    # del my_list
    # import gc
    # gc.collect() # Force GC to see deallocations if tracing continued

    print("--- Profile for process_data ---")
    print(f"Function Result: Processed dict length = {processed_len}")
    print(f"Execution Time: {profile2['time_seconds']:.4f} seconds")
    print(f"Memory Before (traced): {profile2['memory_start_bytes'] / 1024:.2f} KiB")
    print(f"Memory After (traced): {profile2['memory_end_bytes'] / 1024:.2f} KiB")
    print(f"Memory Peak (traced): {profile2['memory_peak_bytes'] / 1024:.2f} KiB")
    print(
        f"Net Memory Diff (traced): {profile2['memory_allocated_diff_bytes'] / 1024:.2f} KiB"
    )
    print("Top 5 Memory Allocation Differences:")
    for alloc_stat in profile2["top_allocations"]:
        print(
            f"  - File: {alloc_stat['filename']}, Line: {alloc_stat['lineno']}, "
            f"Size Diff: {alloc_stat['size_diff_bytes']} bytes, "
            f"Count Diff: {alloc_stat['count_diff']}"
        )

    # Example showing proportionality (roughly)
    print("\n" + "=" * 40 + "\n")
    print("Running with 2x list size:")
    my_list_2x, profile_2x = create_large_list(list_size * 2)
    print("\n--- Profile for create_large_list (2x size) ---")
    print(f"Memory Peak (traced): {profile_2x['memory_peak_bytes'] / 1024:.2f} KiB")
    print(
        f"Net Memory Diff (traced): {profile_2x['memory_allocated_diff_bytes'] / 1024:.2f} KiB"
    )

    print(
        f"\nRatio of Peak Memory (2x / 1x): {profile_2x['memory_peak_bytes'] / profile1['memory_peak_bytes']:.2f}"
    )
    print(
        f"Ratio of Net Diff (2x / 1x): {profile_2x['memory_allocated_diff_bytes'] / profile1['memory_allocated_diff_bytes']:.2f}"
    )
