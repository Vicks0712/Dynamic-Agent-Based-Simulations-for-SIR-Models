import streamlit as st
from src.webapp.views.sirv.components.Animation import Animation
from src.webapp.views.sirv.components.Controls import Controls
from src.webapp.views.sirv.components.Parameters import Parameters
from src.webapp.views.sirv.components.Session import Session
from src.webapp.views.sirv.components.SIRVGraph import SIRVGraph
from src.webapp.views.sirv.components.PopulationGraph import PopulationGraph
from src.back.agents.BaseAgent import State
from src.back.models.sirv_model import SIRVModel


class SIRVModelView:
    """
    View class for the SIR Model simulation with customizable parameters.
    """

    def __init__(self):
        self.params = None
        self.graph_placeholder = None
        self.sirsv_placeholder = None

    def initialize_view(self):
        """Set up the initial view with title, description, and parameters."""
        st.title("SIRV Model Simulation 🦠")
        st.subheader(
            "Simulate the spread of a sir in a network using the SIRV model. "
            "Adjust the parameters to observe how the different states propagates over time."
        )
        Session.initialize_session(Parameters.DEFAULT_PARAMS)
        self.params = Parameters("SIR Model").render()

    def create_model(self):
        """Create a new SIRSV model with current parameters."""
        return SIRVModel(
            num_nodes=self.params["Population (nodes)"],
            avg_node_degree=self.params["Average Node Degree"],
            initial_outbreak_size=self.params["Initial Infected Agents"],
            virus_spread_chance=self.params["Virus Spread Chance"],
            virus_check_frequency=self.params["Virus Check Frequency"],
            recovery_chance=self.params["Recovery Chance"],
            gain_resistance_chance=self.params["Gain Resistance Chance"],
            vaccination_rate=self.params["Vaccination Rate"],
            vaccination_effectiveness=self.params["Vaccination Effectiveness"],
            vaccination_strategy=self.params["Vaccination Strategy"],
            seed=self.params["Random Seed"],
        )

    def initialize_model(self):
        """Initialize the SIR model if it doesn't already exist."""
        if st.session_state.sirsv_model is None:
            st.session_state.sirsv_model = self.create_model()

            # Actualizar los datos iniciales del gráfico
            model = st.session_state.sirsv_model
            st.session_state.sirsv_data["Susceptible"].append(model.number_state(State.SUSCEPTIBLE))
            st.session_state.sirsv_data["Infected"].append(model.number_state(State.INFECTED))
            st.session_state.sirsv_data["Recovered"].append(model.number_state(State.RECOVERED))
            st.session_state.sirsv_data["Vaccinated"].append(model.number_state(State.VACCINATED))

    def update_sirsv_data(self):
        """Update the session state with new population data and print counts."""
        model = st.session_state.sirsv_model
        susceptible = model.number_state(State.SUSCEPTIBLE)
        infected = model.number_state(State.INFECTED)
        resistant = model.number_state(State.RECOVERED)
        vaccinated = model.number_state(State.VACCINATED)

        # Actualizar los datos en la sesión
        st.session_state.sirsv_data["Susceptible"].append(susceptible)
        st.session_state.sirsv_data["Infected"].append(infected)
        st.session_state.sirsv_data["Recovered"].append(resistant)
        st.session_state.sirsv_data["Vaccinated"].append(vaccinated)

    def update_graphs(self):
        """Update both the network and population graphs."""
        self.graph_placeholder.pyplot(SIRVGraph.plot(st.session_state.sirsv_model, self.params["Graph Layout"]))
        self.sirsv_placeholder.pyplot(PopulationGraph.plot(st.session_state.sirsv_data))

    def render_graph_placeholders(self):
        """Render placeholders for the graphs."""
        col1, col2 = st.columns(2)
        self.graph_placeholder = col1.empty()
        self.sirsv_placeholder = col2.empty()

    def initialize_graphs(self):
        """Initialize the graphs with the first render."""
        self.update_graphs()

    def update_network_graph(self):
        """Update only the network graph."""
        self.graph_placeholder.pyplot(SIRVGraph.plot(st.session_state.sirsv_model, self.params["Graph Layout"]))

    def update_population_graph(self):
        """Update only the population graph."""
        self.sirsv_placeholder.pyplot(PopulationGraph.plot(st.session_state.sirsv_data))

    def render_controls(self):
        """Render the control buttons using the Controls class."""
        Controls.render(
            model=st.session_state.sirsv_model,
            update_data_callback=self.update_sirsv_data,
            graph_callbacks=(self.update_network_graph, self.update_population_graph),  # Corregido
            create_model_callback=self.create_model,
        )

    def run_animation(self):
        """Run the animation using the Animation class."""
        if st.session_state.is_playing_sirsv:
            Animation.run(
                model=st.session_state.sirsv_model,
                update_data_callback=self.update_sirsv_data,
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
