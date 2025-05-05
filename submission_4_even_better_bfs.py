import sys
from collections import deque


def solve(n, shortcuts):
    dist = [float("inf")] * n
    dist[0] = 0

    queue = deque([0])

    while queue:
        u = queue.popleft()
        # Calculate next_dist based on the finalized distance of u
        next_dist = dist[u] + 1

        # --- Inlined Neighbor Processing ---
        # Left neighbor
        v_left = u - 1  # Micro-optimization: Assign directly
        if u > 0 and dist[v_left] == float("inf"):
            dist[v_left] = next_dist
            queue.append(v_left)

        # Right neighbor
        v_right = u + 1  # Micro-optimization: Assign directly
        if u < n - 1 and dist[v_right] == float("inf"):
            dist[v_right] = next_dist
            queue.append(v_right)

        # Shortcut neighbor
        # Calculation and bounds check are necessary
        v_shortcut = shortcuts[u] - 1
        if 0 <= v_shortcut < n and dist[v_shortcut] == float("inf"):
            dist[v_shortcut] = next_dist
            queue.append(v_shortcut)
        # --- End Inlined ---

    return [int(d) for d in dist]


n_main = int(sys.stdin.readline())
shortcuts_main = list(map(int, sys.stdin.readline().split()))
final_distances = solve(n_main, shortcuts_main)
print(" ".join(map(str, final_distances)))
