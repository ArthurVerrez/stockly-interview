import streamlit as st
import graphviz
import re  # For parsing input
from collections import deque  # Needed for reconstructing path
from solution import (
    solve,
    get_neighbors,
)  # Import your solver function and neighbor getter
from test_runner import test_cases  # Import test cases for presets

st.set_page_config(layout="wide")
st.title("Mike and Shortcuts - Graph Visualizer & Solver")

st.write(
    "This app visualizes the intersections and shortcuts, then calculates the shortest path from intersection 1 to all others using Breadth-First Search (BFS)."
)

# --- Load Presets ---
preset_options = {
    f"Test Case {i+1} (n={case['n']})": case for i, case in enumerate(test_cases)
}
preset_options["Custom"] = {"n": 5, "shortcuts": [1, 2, 3, 4, 5]}  # Default custom

# --- User Input ---
st.sidebar.header("Input Parameters")

# Preset Selector
selected_preset_key = st.sidebar.selectbox(
    "Load Preset:", options=["Custom"] + list(preset_options.keys())
)

# Get n and shortcuts based on preset or custom input
if selected_preset_key != "Custom":
    preset_data = preset_options[selected_preset_key]
    n_value = preset_data["n"]
    shortcuts_value_list = preset_data["shortcuts"]
    shortcuts_value_str = ", ".join(map(str, shortcuts_value_list))
    st.sidebar.markdown(f"_(Preset **{selected_preset_key}** loaded)_")
else:
    n_value = 5  # Default for custom
    shortcuts_value_str = "1, 2, 3, 4, 5"  # Default for custom


n_input = st.sidebar.number_input(
    "Number of Intersections (n)",
    min_value=1,
    value=n_value,  # Use preset or default
    step=1,
    key=f"n_input_{selected_preset_key}",  # Key changes on preset selection to update value
    help="Total number of intersections (nodes).",
)

shortcuts_input_str = st.sidebar.text_area(
    "Shortcuts List (a_1, a_2, ..., a_n)",
    value=shortcuts_value_str,  # Use preset or default
    key=f"shortcuts_input_{selected_preset_key}",  # Key changes on preset selection to update value
    help="Enter the shortcut destinations for each intersection (1 to n), separated by commas. E.g., for n=3, input might be '2, 2, 3'.",
)

# Add a button to trigger calculation and display
run_button = st.sidebar.button("Visualize and Solve")

# --- Visualization and Solving Area ---
col1, col2 = st.columns(2)


def parse_shortcuts(input_str: str, expected_length: int) -> list[int] | None:
    """Parses the comma-separated shortcut string and validates it."""
    try:
        # Remove extra whitespace, split by comma, filter empty strings
        items = [item.strip() for item in input_str.split(",") if item.strip()]
        if not items:
            st.error("Shortcut input is empty.")
            return None

        shortcuts = [int(item) for item in items]

        if len(shortcuts) != expected_length:
            st.error(
                f"Error: Expected {expected_length} shortcut values, but got {len(shortcuts)}."
            )
            return None
        # Adjust validation: shortcuts are 1-based indices in the input
        if not all(1 <= val <= expected_length for val in shortcuts):
            st.warning(  # Changed to warning as some test cases might have shortcuts outside 1..n, though problem implies they shouldn't
                f"Warning: Some shortcut values are outside the range [1, {expected_length}]. Ensure this is intended."
            )
        # if not all(1 <= val <= expected_length for val in shortcuts):
        #     st.error(
        #         f"Error: All shortcut values must be between 1 and {expected_length}."
        #     )
        #     return None
        return shortcuts
    except ValueError:
        st.error("Error: Shortcuts must be a list of integers separated by commas.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during parsing: {e}")
        return None


def create_initial_graph(n: int, shortcuts: list[int]) -> graphviz.Graph:
    """Creates the Graphviz object for the initial structure."""
    dot = graphviz.Graph(comment="Initial Graph Structure", engine="dot")
    dot.attr(rankdir="LR", size="10,5", ratio="compress")  # Allow more horizontal space

    # Add nodes (1-based)
    for i in range(1, n + 1):
        dot.node(str(i), label=f"Node {i}")

    # Add adjacency edges (i -> i+1 and i+1 -> i) - directed
    for i in range(1, n):
        dot.edge(
            str(i),
            str(i + 1),
            color="gray",
            arrowhead="normal",
            arrowtail="none",
            dir="forward",
        )
        dot.edge(
            str(i + 1),
            str(i),
            color="gray",
            arrowhead="normal",
            arrowtail="none",
            dir="forward",
        )

    # Add shortcut edges (i -> shortcuts[i-1]) - directed
    for i in range(1, n + 1):
        target_node = shortcuts[i - 1]  # This is 1-based from input
        # Only draw shortcut if it's not to itself and valid
        if 1 <= target_node <= n and i != target_node:
            dot.edge(
                str(i),
                str(target_node),
                color="blue",
                style="dashed",
                # label=f"shortcut {i}->{target_node}", # Keep labels concise
                tooltip=f"Shortcut from {i} to {target_node}",
            )

    return dot


def create_result_graph(
    n: int, shortcuts: list[int], distances: list[int]
) -> graphviz.Graph:
    """Creates the Graphviz object showing shortest path steps and distances."""
    dot = graphviz.Graph(comment="Shortest Path Steps", engine="dot")
    dot.attr(
        rankdir="TB", size="8,10", ratio="compress"
    )  # Vertical layout often better for paths

    # Add nodes (1-based) and label with distances
    for i in range(1, n + 1):
        dist = distances[i - 1]  # 0-indexed distances list
        label = f"Node {i}\nDist: {dist}" if dist != -1 else f"Node {i}\nDist: ∞"
        color = (
            "lightblue" if dist == 0 else ("lightcoral" if dist == -1 else "lightgray")
        )  # Highlight start and unreachable
        dot.node(str(i), label=label, style="filled", fillcolor=color)

    # Reconstruct and add edges representing the shortest path tree
    # We need to check potential predecessors for each node
    queue = deque([0])  # Start BFS again conceptually from node 0 (index for node 1)
    visited_edges = set()  # Avoid drawing duplicate edges if multiple paths lead

    processed_for_edges = {0}  # Nodes whose outgoing edges we've considered

    # We check neighbors based on the *original* graph structure
    # to see if the distance matches the BFS requirement (dist[v] == dist[u] + 1)

    nodes_to_process = deque([0])  # Start BFS from the source (index 0)
    processed_nodes = {0}

    while nodes_to_process:
        u_idx = nodes_to_process.popleft()  # 0-based index
        u_node = u_idx + 1  # 1-based node number
        current_dist = distances[u_idx]

        if current_dist == -1:
            continue  # Cannot reach neighbors from here

        # Get potential neighbors based on original graph rules
        # Use the same get_neighbors logic as the solver, adjusted for 0-based index internally
        potential_neighbors_indices = get_neighbors(
            u_idx, n, shortcuts
        )  # Expects 0-based u_idx

        for v_idx in potential_neighbors_indices:  # v_idx is 0-based
            v_node = v_idx + 1  # 1-based node number
            # Check if this neighbor is actually the *next* step in a shortest path
            if distances[v_idx] == current_dist + 1:
                edge = tuple(sorted((u_node, v_node)))  # Use 1-based for edge tracking
                # Check if adding this edge makes sense (part of shortest path)
                # Draw edge from u to v
                dot.edge(str(u_node), str(v_node), color="red", penwidth="1.5")
                if v_idx not in processed_nodes:
                    processed_nodes.add(v_idx)
                    nodes_to_process.append(v_idx)

    return dot


if run_button:
    # st.header("Processing...") # Removed
    shortcuts_list = parse_shortcuts(shortcuts_input_str, n_input)

    if shortcuts_list:
        try:
            # --- Solve first ---
            # We need distances to build the result graph correctly
            calculated_distances = solve(n_input, shortcuts_list)
            # Convert float('inf') back to -1 if necessary (solve might return ints directly now)
            final_distances = [
                int(d) if d != float("inf") else -1 for d in calculated_distances
            ]

            with col1:
                st.subheader("Initial Graph Structure")
                st.write(
                    "Gray edges: adjacent moves (i ⇄ i+1). Blue dashed: shortcuts (i → aᵢ)."
                )
                # st.write("Blue dashed edges show shortcuts (i → aᵢ).") # Combined above
                initial_graph_dot = create_initial_graph(n_input, shortcuts_list)
                st.graphviz_chart(initial_graph_dot)

            with col2:
                st.subheader("Shortest Path Results")
                st.write(
                    "Red arrows show steps taken in the shortest paths from Node 1."
                )
                st.write(f"Min Distances: `{final_distances}`")  # Use final_distances

                # Pass shortcuts too, needed by get_neighbors
                result_graph_dot = create_result_graph(
                    n_input, shortcuts_list, final_distances
                )
                st.graphviz_chart(result_graph_dot)

            st.success("Calculation and visualization complete!")

        except ModuleNotFoundError as e:
            if "test_runner" in str(e):
                st.error(
                    "Error: Could not import `test_cases` from `test_runner.py`. Make sure `test_runner.py` is in the same directory as `app.py` or accessible in the Python path."
                )
            else:
                st.error(f"A required module was not found: {e}")
        except ImportError as e:
            if "get_neighbors" in str(e):
                st.error(
                    "Error: Could not import `get_neighbors` from `solution.py`. Make sure it's defined correctly in `solution.py`."
                )
            else:
                st.error(f"An import error occurred: {e}")
        except Exception as e:
            st.error(f"An error occurred during solving or visualization: {e}")
            import traceback

            st.exception(traceback.format_exc())
    else:
        # Error messages handled within parse_shortcuts
        pass

else:
    st.info(
        "Adjust parameters in the sidebar or select a preset, then click 'Visualize and Solve'."
    )

# --- Add requirements ---
# You might need to install these: pip install streamlit graphviz
# Also ensure the graphviz binary is installed on your system (e.g., `brew install graphviz` on macOS, `sudo apt-get install graphviz` on Debian/Ubuntu)
