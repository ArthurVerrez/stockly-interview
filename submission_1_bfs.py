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

    # Filter out None values (though none are added in this version)
    # and ensure neighbors are within bounds [0, n-1]
    # Note: Shortcut target validity check (within bounds) is implicitly
    # handled by the main loop's distance check. Adding explicit checks
    # here might be slightly safer depending on input constraints.
    valid_neighbors = [
        neighbor for neighbor in neighbors if neighbor is not None and 0 <= neighbor < n
    ]
    # Remove duplicates that might arise if shortcut is adjacent
    return list(set(valid_neighbors))


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

        neighbors = get_neighbors(u, n, shortcuts)
        for v in neighbors:
            # If we found a shorter path to v (or first time visiting)
            if dist[v] == float("inf"):  # In BFS, first time visiting is shortest
                dist[v] = current_dist + 1
                queue.append(v)

    # Convert distances to int for the final result
    return [int(d) for d in dist]


if __name__ == "__main__":
    # Read input in the main block
    n_main = inp()
    shortcuts_main = inlt()

    # Call the core logic function
    final_distances = solve(n_main, shortcuts_main)

    # Print the result
    print(" ".join(map(str, final_distances)))
