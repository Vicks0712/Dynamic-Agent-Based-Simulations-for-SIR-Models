import matplotlib.pyplot as plt


class PopulationGraph:
    """
    Handles the visualization of the population's SEIRV dynamics over time.
    """

    @staticmethod
    def plot(data):
        """
        Plot the SEIR dynamics over time.

        Args:
            data: Dictionary containing time-series data for "Susceptible", "Infected", and "Resistant".

        Returns:
            matplotlib.figure.Figure: The plotted graph.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data["Susceptible"], label="Susceptible (S)", color="blue", linewidth=2, linestyle="--")
        ax.plot(data["Infected"], label="Infected (I)", color="orange", linewidth=2, linestyle="-")
        ax.plot(data["Recovered"], label="Recovered (R)", color="green", linewidth=2, linestyle="-.")
        ax.plot(data["Vaccinated"], label="Vaccinated (V)", color="purple", linewidth=2, linestyle=":")
        ax.plot(data["Exposed"], label="Exposed (E)", color="red", linewidth=2, linestyle="--")
        ax.set_xlabel("Time Steps", fontsize=12)
        ax.set_ylabel("Population Count", fontsize=12)
        ax.set_title("SEIR Model Over Time", fontsize=14, fontweight="bold")
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(alpha=0.6)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        plt.tight_layout()
        return fig

