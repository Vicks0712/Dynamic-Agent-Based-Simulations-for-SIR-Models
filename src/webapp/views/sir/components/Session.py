import streamlit as st

class Session:
    """
    A class to manage the session state for the SIR model application.

    This class initializes and manages the session state variables required for the SIR model simulation.

    Methods
    -------
    initialize_session():
        Initializes the session state variables for the SIR model simulation.
    """

    @staticmethod
    def initialize_session(default_params):
        """
        Initializes the session state variables for the SIR model simulation.

        Args:
            default_params (dict): Default parameters for the SIR model.
        """
        if "sirsv_model" not in st.session_state:
            st.session_state.sirsv_model = None
            st.session_state.sirsv_data = {
                "Susceptible": [],
                "Infected": [],
                "Recovered": [],
                "Vaccinated": []
            }
            st.session_state.is_playing_sirsv = False

        # Set default parameters if not already set
        for key, value in default_params.items():
            if key not in st.session_state:
                st.session_state[key] = value
