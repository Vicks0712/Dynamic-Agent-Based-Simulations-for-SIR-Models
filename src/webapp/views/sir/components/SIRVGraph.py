import matplotlib.pyplot as plt
import networkx as nx

from src.back.agents.BaseAgent import State


class SIRVGraph:
    """
    Handles the visualization of the SIR model's network graph.
    """

    @staticmethod
    def plot(model, layout):
        """
        Plot the graph representing the model's network.

        Args:
            model: The SIRVModel instance. If None, plots a default graph.
            layout: The layout type for the graph (e.g., "spring", "circular", "kamada-kawai").

        Returns:
            matplotlib.figure.Figure: The plotted graph.
        """
        if model is None:
            # Generate a default placeholder graph
            G = nx.erdos_renyi_graph(n=10, p=0.2, seed=42)  # Small example graph
            pos = nx.spring_layout(G, iterations=5, seed=8)
            node_colors = ["gray"] * len(G.nodes)
        else:
            # Use the model's graph
            G = model.G
            if layout == "kamada-kawai":
                pos = nx.kamada_kawai_layout(G)
            elif layout == "circular":
                pos = nx.circular_layout(G)
            else:
                pos = nx.spring_layout(G, iterations=5, seed=8)

            # Set node colors based on agent states
            node_colors = []
            for node in G.nodes:
                agents = model.grid.get_cell_list_contents([node])
                if agents:
                    state = agents[0].state
                    node_colors.append(
                        "orange" if state == State.INFECTED else
                        "lightblue" if state == State.SUSCEPTIBLE else
                        "green" if state == State.RECOVERED else
                        "purple"
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
        plt.close(fig)
        return fig
