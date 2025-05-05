import streamlit as st
import graphviz
import re  # For parsing input
from solution import solve  # Import your solver function

st.set_page_config(layout="wide")
st.title("Mike and Shortcuts - Graph Visualizer & Solver")

st.write(
    "This app visualizes the intersections and shortcuts, then calculates the shortest path from intersection 1 to all others using Breadth-First Search (BFS)."
)

# --- User Input ---
st.sidebar.header("Input Parameters")
n_input = st.sidebar.number_input(
    "Number of Intersections (n)",
    min_value=1,
    value=5,
    step=1,
    help="Total number of intersections (nodes).",
)

shortcuts_input_str = st.sidebar.text_area(
    "Shortcuts List (a_1, a_2, ..., a_n)",
    value="1, 2, 3, 4, 5",
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
        if not all(1 <= val <= expected_length for val in shortcuts):
            st.error(
                f"Error: All shortcut values must be between 1 and {expected_length}."
            )
            return None
        return shortcuts
    except ValueError:
        st.error("Error: Shortcuts must be a list of integers separated by commas.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during parsing: {e}")
        return None


def create_initial_graph(n: int, shortcuts: list[int]) -> graphviz.Graph:
    """Creates the Graphviz object for the initial structure."""
    dot = graphviz.Graph(
        comment="Initial Graph Structure", engine="dot"
    )  # Use 'dot' for hierarchical, 'neato' or 'fdp' for spring layouts
    dot.attr(rankdir="LR", size="8,5")  # Arrange left-to-right

    # Add nodes (1-based)
    for i in range(1, n + 1):
        dot.node(str(i), label=f"Node {i}")

    # Add adjacency edges (i <-> i+1) - undirected
    for i in range(1, n):
        dot.edge(
            str(i), str(i + 1), dir="both", color="gray"
        )  # Use dir='both' for undirected look

    # Add shortcut edges (i -> shortcuts[i-1]) - directed
    for i in range(1, n + 1):
        target_node = shortcuts[i - 1]
        # Only draw shortcut if it's not to itself (optional, but cleaner)
        if i != target_node:
            dot.edge(
                str(i),
                str(target_node),
                color="blue",
                style="dashed",
                label=f"shortcut from {i}",
            )

    return dot


def create_result_graph(n: int, distances: list[int]) -> graphviz.Graph:
    """Creates the Graphviz object showing nodes with distances."""
    dot = graphviz.Graph(comment="Shortest Path Distances", engine="dot")
    dot.attr(rankdir="LR", size="8,5")

    # Add nodes (1-based) and label with distances
    for i in range(1, n + 1):
        dist = distances[i - 1]  # 0-indexed distances list
        label = f"Node {i}\nDist: {dist}" if dist != -1 else f"Node {i}\nDist: ∞"
        color = "lightblue" if dist == 0 else "lightgray"  # Highlight start node
        dot.node(str(i), label=label, style="filled", fillcolor=color)

    # Optional: Could add edges representing the actual shortest path tree,
    # but just showing distances on nodes fulfills the request.

    return dot


if run_button:
    st.header("Processing...")
    shortcuts_list = parse_shortcuts(shortcuts_input_str, n_input)

    if shortcuts_list:
        try:
            with col1:
                st.subheader("Initial Graph Structure")
                st.write("Gray edges connect adjacent nodes (i ↔ i+1).")
                st.write("Blue dashed edges show shortcuts (i → aᵢ).")
                initial_graph_dot = create_initial_graph(n_input, shortcuts_list)
                st.graphviz_chart(initial_graph_dot)

            # --- Solve ---
            calculated_distances = solve(n_input, shortcuts_list)

            with col2:
                st.subheader("Shortest Path Results")
                st.write("Minimum steps (distance) from Node 1 to all other nodes.")
                st.write(f"Calculated Distances: `{calculated_distances}`")

                result_graph_dot = create_result_graph(n_input, calculated_distances)
                st.graphviz_chart(result_graph_dot)

            st.success("Calculation and visualization complete!")

        except Exception as e:
            st.error(f"An error occurred during solving or visualization: {e}")
            import traceback

            st.exception(traceback.format_exc())
    else:
        # Error messages handled within parse_shortcuts
        pass

else:
    st.info("Adjust parameters in the sidebar and click 'Visualize and Solve'.")

# --- Add requirements ---
# You might need to install these: pip install streamlit graphviz
# Also ensure the graphviz binary is installed on your system (e.g., `brew install graphviz` on macOS, `sudo apt-get install graphviz` on Debian/Ubuntu)
