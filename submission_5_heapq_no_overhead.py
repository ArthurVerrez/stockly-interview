import sys
import heapq

input = sys.stdin.readline


# --- Core Logic Function (Dijkstra with heapq) ---
def solve(n, shortcuts_1_based):
    """Solves the shortest path problem using Dijkstra's algorithm with a priority queue.

    Args:
        n: The number of intersections.
        shortcuts_1_based: A list where shortcuts_1_based[i] is the 1-based destination
                           from intersection i+1.

    Returns:
        A list of n integers representing the minimum distance from node 1
        to every other node (0-indexed list for nodes 0 to n-1).
    """
    # Initialize distances: infinite for all nodes except the start (node 0)
    dist = [float("inf")] * n
    dist[0] = 0  # Distance to node 1 (index 0) is 0

    # Priority Queue: stores tuples of (current_distance, node_index)
    # Initialize with the source node (distance 0, node index 0)
    # heapq implements a min-heap, perfect for Dijkstra.
    pq = [(0, 0)]

    while pq:
        # Pop the node with the smallest tentative distance from the priority queue
        d, u = heapq.heappop(pq)

        # ----- Dijkstra's Optimization: Staleness Check -----
        # If the distance 'd' from the priority queue is already greater than
        # the shortest distance we've recorded for node 'u', then this queue entry
        # is outdated (we found a shorter path earlier). Skip processing.
        if d > dist[u]:
            continue
        # ----------------------------------------------------

        # Explore neighbors of node u. The cost for each valid move is 1.
        edge_cost = 1
        current_dist_to_u = dist[u]  # This should be equal to d if not stale

        # --- Neighbor Generation and Relaxation ---

        # 1. Check left neighbor (u-1)
        v_left = u - 1
        if v_left >= 0:
            new_dist_to_v = current_dist_to_u + edge_cost
            # Relaxation: If the path through u is shorter than the known distance to v_left
            if new_dist_to_v < dist[v_left]:
                dist[v_left] = new_dist_to_v
                heapq.heappush(pq, (new_dist_to_v, v_left))

        # 2. Check right neighbor (u+1)
        v_right = u + 1
        if v_right < n:
            new_dist_to_v = current_dist_to_u + edge_cost
            # Relaxation
            if new_dist_to_v < dist[v_right]:
                dist[v_right] = new_dist_to_v
                heapq.heappush(pq, (new_dist_to_v, v_right))

        # 3. Check shortcut neighbor
        # Get the 1-based target from the input list using 0-based index u
        shortcut_target_1_based = shortcuts_1_based[u]
        # Convert the target to a 0-based index
        v_shortcut = shortcut_target_1_based - 1

        # Check bounds of the shortcut target
        if 0 <= v_shortcut < n:
            new_dist_to_v = current_dist_to_u + edge_cost
            # Relaxation
            if new_dist_to_v < dist[v_shortcut]:
                dist[v_shortcut] = new_dist_to_v
                heapq.heappush(pq, (new_dist_to_v, v_shortcut))
        # --- End Neighbor Generation and Relaxation ---

    # Convert final distances to integers
    return [int(d) for d in dist]


n_main = int(sys.stdin.readline())
shortcuts_main = list(map(int, sys.stdin.readline().split()))
final_distances = solve(n_main, shortcuts_main)
print(" ".join(map(str, final_distances)))
