# solution.py
import sys
from collections import deque
from typing import List, Optional


# Utility functions for standard competitive programming input
# Keep these separate for the __main__ block
def _input() -> str:
    return sys.stdin.readline()


def inp() -> int:
    """Reads an integer from stdin."""
    return int(_input())


def inlt() -> List[int]:
    """Reads a list of integers from stdin."""
    return list(map(int, _input().split()))


def get_neighbors(node: int, n: int, shortcuts: List[int]) -> List[int]:
    """Gets valid neighbors for a given node."""
    neighbors: List[Optional[int]] = []

    # Add left neighbor if it exists
    if node > 0:
        neighbors.append(node - 1)

    # Add right neighbor if it exists
    if node < n - 1:
        neighbors.append(node + 1)

    # Add shortcut neighbor if it exists and is different from the node itself
    shortcut_target = shortcuts[node] - 1  # Adjust to 0-based index
    if shortcut_target != node:
        neighbors.append(shortcut_target)

    # Filter out None values and ensure neighbors are within bounds [0, n-1]
    valid_neighbors = [
        neighbor for neighbor in neighbors if neighbor is not None and 0 <= neighbor < n
    ]
    # Remove duplicates that might arise if shortcut is adjacent
    return list(set(valid_neighbors))


# --- Core Logic Function (Testable) ---
def solve(n: int, shortcuts: List[int]) -> List[int]:
    """
    Solves the shortest path problem using BFS.

    Args:
        n: The number of intersections.
        shortcuts: A list where shortcuts[i] is the destination
                           from intersection i+1 (using 1-based indexing from problem).

    Returns:
        A list of n integers representing the minimum cost (number of steps)
        from node 1 to every other node (1-based result corresponding to nodes 1 to n).
        The list itself is 0-indexed (dist[0] for node 1, dist[n-1] for node n).
    """
    dist: List[float] = [float("inf")] * n
    dist[0] = 0

    queue = deque([0])  # Queue stores nodes to visit (0-indexed)

    while queue:
        u = queue.popleft()
        current_dist = dist[u]

        neighbors = get_neighbors(u, n, shortcuts)
        for v in neighbors:
            # If we found a shorter path to v (or first time visiting)
            if dist[v] == float("inf"):  # In BFS, first time visiting is shortest
                dist[v] = current_dist + 1
                queue.append(v)

    # Convert distances to int for the final result
    result_dist = [
        int(d) if d != float("inf") else -1 for d in dist
    ]  # Assuming unreachable nodes should be -1 or similar? Adjust if needed. The example used int(d).
    # Let's stick to the example's direct int conversion for now.
    result_dist = [int(d) for d in dist]

    return result_dist


# --- Main execution block for direct running (e.g., competitive programming) ---
if __name__ == "__main__":
    n_main = inp()
    shortcuts_main = inlt()

    # Call the core logic function
    final_distances = solve(n_main, shortcuts_main)

    # Print the result in the required format
    print(" ".join(map(str, final_distances)))
