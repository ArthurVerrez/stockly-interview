# test_runner.py
import sys
import os
from typing import List, Dict, Any
from utils.profile_performance import profile_memory_and_time

from submission_1_bfs import solve

# --- Test Case Definition ---
# Each test case is a dictionary with input and expected output.
test_cases: List[Dict[str, Any]] = [
    {
        "n": 3,
        "shortcuts": [2, 2, 3],  # a1, a2, a3
        "expected_output": [0, 1, 2],  # m1, m2, m3
    },
    {
        "n": 5,
        "shortcuts": [1, 2, 3, 4, 5],
        "expected_output": [0, 1, 2, 3, 4],
    },
    {
        "n": 7,
        "shortcuts": [4, 4, 4, 4, 7, 7, 7],
        "expected_output": [0, 1, 2, 1, 2, 3, 3],
    },
    {
        "n": 4,
        "shortcuts": [1, 2, 3, 4],
        "expected_output": [0, 1, 2, 3],
    },
    {
        "n": 6,
        "shortcuts": [2, 3, 4, 5, 6, 6],
        "expected_output": [0, 1, 2, 3, 4, 5],
    },
    # Add more test cases if needed
    {
        "n": 98,
        "shortcuts": [
            17,
            17,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            57,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            87,
            90,
            90,
            90,
            90,
            90,
            90,
            90,
            90,
            90,
            90,
            90,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            92,
            95,
            95,
            95,
            95,
            95,
            97,
            98,
            98,
        ],
        "expected_output": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            8,
            7,
            6,
            5,
            4,
            3,
            2,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            21,
            20,
            19,
            18,
            17,
            16,
            15,
            14,
            13,
            12,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            18,
            17,
            16,
            15,
            14,
            13,
            12,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            4,
            4,
            5,
            6,
            5,
            6,
            7,
            8,
        ],
    },
    {
        "n": 91,
        "shortcuts": [
            4,
            6,
            23,
            23,
            23,
            23,
            23,
            28,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            39,
            47,
            47,
            47,
            54,
            54,
            54,
            54,
            54,
            54,
            54,
            58,
            58,
            58,
            58,
            58,
            58,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            69,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            71,
            72,
            72,
            72,
            73,
            75,
            77,
            77,
            77,
            82,
            82,
            84,
            84,
            84,
            84,
            84,
            85,
            86,
            87,
            89,
            89,
            90,
            91,
        ],
        "expected_output": [
            0,
            1,
            2,
            1,
            2,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            2,
            3,
            4,
            5,
            6,
            5,
            6,
            7,
            8,
            9,
            9,
            8,
            7,
            6,
            5,
            4,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            9,
            10,
            9,
            8,
            7,
            6,
            5,
            4,
            5,
            6,
            7,
            6,
            7,
            8,
            9,
            10,
            11,
            10,
            9,
            8,
            7,
            6,
            5,
            6,
            6,
            7,
            8,
            9,
            10,
            11,
            11,
            12,
            13,
            14,
            14,
            13,
            14,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
        ],
    },
]


# --- Helper Function for Formatting ---
def format_bytes(size_bytes: int) -> str:
    """Converts bytes to a readable format (KiB, MiB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KiB"
    else:
        return f"{size_bytes / (1024**2):.2f} MiB"


# --- Test Runner Logic ---
def run_tests():
    """Runs all defined test cases against the solver."""
    # Apply the decorator here for profiling within the test runner
    profiled_solve = profile_memory_and_time(solve)

    passed_count = 0
    failed_count = 0
    total_count = len(test_cases)

    print("=" * 60)
    print(f"Running {total_count} Test Case(s) for 'Mike and Shortcuts'")
    print("=" * 60)

    for i, case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        n_val = case["n"]
        shortcuts_val = case["shortcuts"]
        expected = case["expected_output"]

        try:
            # Call the decorated function, unpack result and profile info
            actual, profile_info = profiled_solve(n_val, shortcuts_val)

            # Compare results
            if actual == expected:
                print("Status: PASS")
                passed_count += 1
            else:
                print("Status: FAIL")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {actual}")
                failed_count += 1

            # Print performance profile
            print("\n  Performance Profile:")
            print(f"    Execution Time: {profile_info['time_seconds']:.6f} seconds")
            # print(f"    Memory Start:   {format_bytes(profile_info['memory_start_bytes'])}") # Often near 0 or small base
            print(
                f"    Memory Peak:    {format_bytes(profile_info['memory_peak_bytes'])}"
            )
            # print(f"    Memory End:     {format_bytes(profile_info['memory_end_bytes'])}")
            print(
                f"    Net Memory Diff:{format_bytes(profile_info['memory_allocated_diff_bytes'])}"
            )

        except Exception as e:
            print(f"Status: ERROR during execution!")
            print(f"  Error: {type(e).__name__}: {e}")
            import traceback

            print("  Traceback:")
            print(traceback.format_exc(limit=5))  # Limit traceback length
            failed_count += 1

        print("-" * 40)  # Separator for readability

    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Total Cases: {total_count}")
    print(f"  Passed:      {passed_count}")
    print(f"  Failed:      {failed_count}")
    print("=" * 60)

    # Exit with non-zero code if any tests failed/errored
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
