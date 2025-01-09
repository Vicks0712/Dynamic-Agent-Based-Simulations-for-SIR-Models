import matplotlib.pyplot as plt


class PopulationGraph:
    """
    Handles the visualization of the population's SEIRV dynamics over time.
    """

    @staticmethod
    def plot(data):
        """
        Plot the SEIRV dynamics over time.

        Args:
            data: Dictionary containing time-series data for "Susceptible", "Infected", and "Resistant".

        Returns:
            matplotlib.figure.Figure: The plotted graph.
        """
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(data["Susceptible"], label="Susceptible", color="blue")
        ax.plot(data["Infected"], label="Infected", color="orange")
        ax.plot(data["Recovered"], label="Recovered", color="green")
        ax.plot(data["Vaccinated"], label="Vaccinated", color="purple")
        ax.plot(data["Exposed"], label="Exposed", color="red")
        ax.set_xlabel("Steps")
        ax.set_ylabel("Count")
        ax.legend()
        ax.set_title("SEIRV Model Over Time")
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
        return fig
