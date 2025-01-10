import streamlit as st
from src.webapp.views.seirv.components.SEIRVGraph import SEIRVGraph
from src.webapp.views.seirv.components.Animation import Animation
from src.webapp.views.seirv.components.Controls import Controls
from src.webapp.views.seirv.components.Parameters import Parameters
from src.webapp.views.seirv.components.Session import Session
from src.webapp.views.seirv.components.PopulationGraph import PopulationGraph
from src.back.agents.BaseAgent import State
from src.back.models.seir_model import SEIRModel


class SEIRVModelView:
    """
    View class for the SIR Model simulation with customizable parameters.
    """

    def __init__(self):
        self.params = None
        self.graph_placeholder = None
        self.seirv_placeholder = None

    def initialize_view(self):
        """Set up the initial view with title, description, and parameters."""
        st.title("SEIRV Model Simulation 🦠")
        st.subheader(
            "Simulate the spread of a sir in a network using the SEIRV model. Adjust the parameters to observe how the sir propagates over time."
        )
        Session.initialize_session(Parameters.DEFAULT_PARAMS)
        self.params = Parameters("SIR Model").render()

    def create_model(self):
        """Create a new SEIRV model with current parameters."""
        print(self.params["Initial Infected Agents"])
        return SEIRModel(
            num_nodes=self.params["Population (nodes)"],
            avg_node_degree=self.params["Average Node Degree"],
            initial_infected_size=self.params["Initial Infected Agents"],
            initial_exposed_size=self.params["Initial Exposed Agents"],
            virus_spread_chance=self.params["Virus Spread Chance"],
            virus_check_frequency=self.params["Virus Check Frequency"],
            recovery_chance=self.params["Recovery Chance"],
            gain_resistance_chance=self.params["Gain Resistance Chance"],
            exposure_to_infection_chance=self.params["Exposure to infection chance"],
            vaccination_rate=self.params["Vaccination Rate"],
            vaccination_effectiveness=self.params["Vaccination Effectiveness"],
            seed=self.params["Random Seed"],
        )


    def initialize_model(self):
        """Initialize the SIR model if it doesn't already exist."""
        if st.session_state.seirv_model is None:
            st.session_state.seirv_model = self.create_model()

    def update_seirv_data(self):
        """Update the session state with new population data and print counts."""
        model = st.session_state.seirv_model
        susceptible = model.number_state(State.SUSCEPTIBLE)
        infected = model.number_state(State.INFECTED)
        resistant = model.number_state(State.RECOVERED)
        vaccinated = model.number_state(State.VACCINATED)
        exposed = model.number_state(State.EXPOSED)

        # Actualizar los datos en la sesión
        st.session_state.seirv_data["Susceptible"].append(susceptible)
        st.session_state.seirv_data["Infected"].append(infected)
        st.session_state.seirv_data["Recovered"].append(resistant)
        st.session_state.seirv_data["Vaccinated"].append(vaccinated)
        st.session_state.seirv_data["Exposed"].append(exposed)

    def update_graphs(self):
        """Update both the network and population graphs."""
        self.graph_placeholder.pyplot(SEIRVGraph.plot(st.session_state.seirv_model, self.params["Graph Layout"]))
        self.seirv_placeholder.pyplot(PopulationGraph.plot(st.session_state.seirv_data))

    def render_graph_placeholders(self):
        """Render placeholders for the graphs."""
        col1, col2 = st.columns(2)
        self.graph_placeholder = col1.empty()
        self.seirv_placeholder = col2.empty()

    def initialize_graphs(self):
        """Initialize the graphs with the first render."""
        self.update_graphs()

    def update_network_graph(self):
        """Update only the network graph."""
        self.graph_placeholder.pyplot(SEIRVGraph.plot(st.session_state.seirv_model, self.params["Graph Layout"]))

    def update_population_graph(self):
        """Update only the population graph."""
        self.seirv_placeholder.pyplot(PopulationGraph.plot(st.session_state.seirv_data))

    def render_controls(self):
        """Render the control buttons using the Controls class."""
        Controls.render(
            model=st.session_state.seirv_model,
            update_data_callback=self.update_seirv_data,
            graph_callbacks=(self.update_network_graph, self.update_population_graph),  # Corregido
            create_model_callback=self.create_model,
        )

    def run_animation(self):
        """Run the animation using the Animation class."""
        if st.session_state.is_playing_seirv:
            Animation.run(
                model=st.session_state.seirv_model,
                update_data_callback=self.update_seirv_data,
                graph_callbacks=(self.update_network_graph, self.update_population_graph),  # Pasar ambas funciones
                steps=self.params["Steps"],
            )

    def run(self):
        """Main function to run the SIR model view."""
        self.initialize_view()
        self.initialize_model()
        self.render_graph_placeholders()
        self.initialize_graphs()
        self.render_controls()
        self.run_animation()
