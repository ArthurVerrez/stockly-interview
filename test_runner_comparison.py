# test_runner.py
import sys
import os
from typing import List, Dict, Any
from utils.profile_performance import profile_memory_and_time

# Import both solve functions with aliases
from submission_2_heapq import solve as solve_1
from submission_3_better_bfs import solve as solve_2

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
    """Runs all defined test cases against both solvers and compares them."""
    # Apply the decorator to both solve functions
    profiled_solve_bfs = profile_memory_and_time(solve_1)
    profiled_solve_heapq = profile_memory_and_time(solve_2)

    passed_count = 0
    failed_count = 0
    total_count = len(test_cases)

    print("=" * 70)
    print(f"Running {total_count} Test Case(s) Comparison: 1 vs 2")
    print("=" * 70)

    for i, case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        n_val = case["n"]
        shortcuts_val = case["shortcuts"]
        expected = case["expected_output"]

        case_passed = True  # Track overall pass status for this case

        try:
            # --- Run BFS Solver (solve_1) ---
            print("\n  Running Solver 1...")
            actual_solver_1, profile_bfs = profiled_solve_bfs(n_val, shortcuts_val)
            is_solver_1_correct = actual_solver_1 == expected
            print(f"    Status: {'PASS' if is_solver_1_correct else 'FAIL'}")
            if not is_solver_1_correct:
                print(f"      Expected: {expected}")
                print(f"      Actual: {actual_solver_1}")
                case_passed = False

            print("    Performance Profile:")
            print(f"      Execution Time: {profile_bfs['time_seconds']:.6f} seconds")
            print(
                f"      Memory Peak:    {format_bytes(profile_bfs['memory_peak_bytes'])}"
            )
            print(
                f"      Net Memory Diff:{format_bytes(profile_bfs['memory_allocated_diff_bytes'])}"
            )

            # --- Run Heapq Solver (solve_2) ---
            print("\n  Running Solver 2...")
            actual_solver_2, profile_heapq = profiled_solve_heapq(n_val, shortcuts_val)
            is_solver_2_correct = actual_solver_2 == expected
            print(f"    Status: {'PASS' if is_solver_2_correct else 'FAIL'}")
            if not is_solver_2_correct:
                print(f"      Expected: {expected}")
                print(f"      Actual: {actual_solver_2}")
                case_passed = False

            print("    Performance Profile:")
            print(f"      Execution Time: {profile_heapq['time_seconds']:.6f} seconds")
            print(
                f"      Memory Peak:    {format_bytes(profile_heapq['memory_peak_bytes'])}"
            )
            print(
                f"      Net Memory Diff:{format_bytes(profile_heapq['memory_allocated_diff_bytes'])}"
            )

            # --- Compare Results --- (Optional but good practice)
            if (
                is_solver_1_correct
                and is_solver_2_correct
                and actual_solver_1 != actual_solver_2
            ):
                print(
                    "\n  WARNING: Both solvers passed against expected, but produced different results!"
                )
                print(f"    Result 1:   {actual_solver_1}")
                print(f"    Result 2: {actual_solver_2}")
                # Decide if this constitutes a failure for the overall case
                # case_passed = False

            if case_passed:
                passed_count += 1
            else:
                failed_count += 1

        except Exception as e:
            print(f"\nStatus: ERROR during execution for Case {i+1}!")
            print(f"  Error: {type(e).__name__}: {e}")
            import traceback

            print("  Traceback:")
            print(traceback.format_exc(limit=5))  # Limit traceback length
            failed_count += 1
            case_passed = False  # Ensure error marks case as failed

        print("-" * 50)  # Separator for readability

    print("\n" + "=" * 70)
    print("Comparison Test Summary:")
    print(f"  Total Cases: {total_count}")
    print(f"  Cases Passed (Both Solvers Correct): {passed_count}")
    print(f"  Cases Failed (Mismatch or Error):  {failed_count}")
    print("=" * 70)

    # Exit with non-zero code if any tests failed/errored
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
