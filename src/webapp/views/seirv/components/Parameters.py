import streamlit as st

class Parameters:
    """
    A reusable component for configuring model parameters in the main layout.
    """

    DEFAULT_PARAMS = {
        "Population (nodes)": (10, 500, 100, 10),
        "Average Node Degree": (1, 20, 4),
        "Initial Infected Agents": (1, 50, 5),
        "Initial Exposed Agents": (1, 50, 5),
        "Virus Spread Chance": (0.0, 1.0, 0.2, 0.05),
        "Virus Check Frequency": (0.0, 1.0, 0.4, 0.05),
        "Recovery Chance": (0.0, 1.0, 0.3, 0.05),
        "Exposure to infection chance": (0.0, 1.0, 0.3, 0.05),
        "Gain Resistance Chance": (0.0, 1.0, 0.5, 0.05),
        "Vaccination Rate": (0.0, 1.0, 0.05, 0.05),
        "Vaccination Effectiveness": (0.0, 1.0, 0.65, 0.05),
        "Random Seed": 42,
        "Steps": 50,
        "Graph Layout": ["spring", "circular", "kamada-kawai"],
    }

    def __init__(self, model_name, default_params=None):
        """
        Initialize the parameter component.

        Args:
            model_name (str): The name of the model (e.g., SIR, SIRV).
            default_params (dict, optional): A dictionary of default parameters.
                                             If None, uses DEFAULT_PARAMS.
        """
        self.model_name = model_name
        self.default_params = default_params or Parameters.DEFAULT_PARAMS
        self.params = {}

    def render(self):
        """
        Render the parameters component in the main layout and return the user-selected parameters.

        Returns:
            dict: The user-selected parameters.
        """
        # CSS para personalizar el título del expander
        st.markdown(f"""
        <style>
            .custom-expander-title {{
                font-size: 22px !important;
                font-weight: bold !important;
                color: #4a7abc !important;
                margin-top: 20px !important;
            }}
        </style>
        """, unsafe_allow_html=True)

        # Crear el expander en el contenido principal
        with st.expander(f"⚙️ Adjust Parameters for {self.model_name}", expanded=False):
            for key, value in self.default_params.items():
                if isinstance(value, tuple):  # Assuming (min, max, default) for sliders
                    self.params[key] = st.slider(key, value[0], value[1], value[2], step=value[3] if len(value) > 3 else 1)
                elif isinstance(value, list):  # Assuming dropdown options
                    self.params[key] = st.selectbox(key, value, index=value.index(value[-1]) if value[-1] in value else 0)
                else:  # Assuming number inputs for other types
                    self.params[key] = st.number_input(key, value)
        return self.params
