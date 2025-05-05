import sys
from collections import deque
from typing import List, Optional

# Utility function for codeforces
input = sys.stdin.readline


def inp() -> int:
    """Reads an integer from stdin."""
    return int(input())


def inlt() -> List[int]:
    """Reads a list of integers from stdin."""
    return list(map(int, input().split()))


# --- Core Logic Function (BFS) ---
def solve(n: int, shortcuts: List[int]) -> List[int]:
    """Solves the shortest path problem using BFS.

    Args:
        n: The number of intersections.
        shortcuts: A list where shortcuts[i] is the 1-based destination
                   from intersection i+1.

    Returns:
        A list of n integers representing the minimum distance (number of steps)
        from node 1 to every other node (0-indexed list for nodes 0 to n-1).
    """
    dist: List[float] = [float("inf")] * n
    dist[0] = 0

    queue = deque([0])  # Queue stores nodes to visit (0-indexed)

    while queue:
        u = queue.popleft()
        current_dist = dist[u]
        next_dist = current_dist + 1

        # Process potential neighbors directly
        # Left neighbor
        if u > 0:
            v = u - 1
            if dist[v] == float("inf"):
                dist[v] = next_dist
                queue.append(v)

        # Right neighbor
        if u < n - 1:
            v = u + 1
            if dist[v] == float("inf"):
                dist[v] = next_dist
                queue.append(v)

        # Shortcut neighbor
        shortcut_target = shortcuts[u] - 1  # Adjust to 0-based index
        # Check if shortcut leads to a valid and unvisited node
        # (No need to check shortcut_target != u explicitly,
        # as dist[u] is already set, so dist[shortcut_target] wouldn't be inf)
        if 0 <= shortcut_target < n and dist[shortcut_target] == float("inf"):
            dist[shortcut_target] = next_dist
            queue.append(shortcut_target)

    # Convert distances to int for the final result
    # Handle potential unreachable nodes (still inf) if necessary, though
    # problem constraints usually guarantee connectivity.
    # If unreachable nodes should be represented differently (e.g., -1), adjust here.
    return [
        int(d) if d != float("inf") else -1 for d in dist
    ]  # Example: return -1 for unreachable


if __name__ == "__main__":
    # Read input in the main block
    n_main = inp()
    shortcuts_main = inlt()

    # Call the core logic function
    final_distances = solve(n_main, shortcuts_main)

    # Print the result
    print(" ".join(map(str, final_distances)))
