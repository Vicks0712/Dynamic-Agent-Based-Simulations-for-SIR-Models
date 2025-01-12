import matplotlib.pyplot as plt
import networkx as nx
from src.back.agents.BaseAgent import State


class SEIRGraph:
    """
    Handles the visualization of the SEIRV model's network graph.
    """

    @staticmethod
    def plot(model, layout):
        """
        Plot the graph representing the SEIRV model's network.

        Args:
            model: The SEIRVModel instance. If None, plots a default graph.
            layout: The layout type for the graph (e.g., "spring", "circular", "kamada-kawai").

        Returns:
            matplotlib.figure.Figure: The plotted graph.
        """
        layout_functions = {
            "circular": nx.circular_layout,
            "erdos_renyi": lambda G: nx.kamada_kawai_layout(G),  # Default to spring layout
        }

        if model is None:
            # Generate a default placeholder graph
            G = nx.erdos_renyi_graph(n=10, p=0.2, seed=42)  # Small example graph
            pos = nx.spring_layout(G, iterations=5, seed=8)
            node_colors = ["gray"] * len(G.nodes)
        else:
            # Use the model's graph
            G = model.G
            pos = layout_functions.get(layout, layout_functions["erdos_renyi"])(G)

            # Set node colors based on agent states
            node_colors = []
            for node in G.nodes:
                agents = model.grid.get_cell_list_contents([node])
                if agents:
                    state = agents[0].state
                    # Map states to colors
                    node_colors.append(
                        "red" if state == State.EXPOSED else  # Exposed (new)
                        "orange" if state == State.INFECTED else  # Infected (new)
                        "lightblue" if state == State.SUSCEPTIBLE else  # Susceptible
                        "green" if state == State.RECOVERED else  # Resistant
                        "purple" if state == State.VACCINATED else  # Vaccinated
                        "gray"  # Default for unknown states
                    )
                else:
                    node_colors.append("gray")

        # Plot the graph
        fig, ax = plt.subplots(figsize=(5, 4))
        nx.draw(
            G,
            pos,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=200,
            edge_color="gray",
        )
        ax.set_title("SEIRV Model Graph")
        #plt.close(fig)
        return fig
