import streamlit as st

class Controls:
    """
    Handles the control buttons for the simulation (Step, Reset, Play/Pause).
    """

    @staticmethod
    def render(model, update_data_callback, graph_callbacks, create_model_callback):
        """
        Renders the control buttons and handles their logic.

        Args:
            model: The current simulation model.
            update_data_callback: A function to update the population data.
            graph_callbacks: A tuple with graph update functions (update_network_graph, update_population_graph).
            create_model_callback: A function to create a new model based on current parameters.
        """
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Step"):
                model.step()
                update_data_callback()
                graph_callbacks[0]()  # Update network graph
                graph_callbacks[1]()  # Update population graph

        with col2:
            if st.button("Reset"):
                # Reinitialize the model
                st.session_state.seirv_model = create_model_callback()
                st.session_state.seirv_data = {
                    "Susceptible": [],
                    "Infected": [],
                    "Recovered": [],
                    "Vaccinated": [],
                    "Exposed": [],
                }
                st.session_state.is_playing_seirv = False

                # Update graphs with the reset model
                graph_callbacks[0]()  # Reset network graph
                graph_callbacks[1]()  # Reset population graph (empty)

        with col3:
            if st.button("Play/Pause"):
                st.session_state.is_playing_seirv = not st.session_state.is_playing_seirv
