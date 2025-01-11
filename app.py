import streamlit as st
from src.webapp.static_components.SideBar import SideBar
from src.webapp.views.default.DefaultView import DefaultView
from src.webapp.views.seir.SEIRModelView import SEIRModelView
from src.webapp.views.sirs.SIRSModelView import SIRSModelView
from src.webapp.views.sir.SIRModelView import SIRModelView

st.set_page_config(
    page_title="Virus Simulation Suite",
    page_icon="🦠",
    layout="wide"
)

class MultiApp:
    """
    Main class to manage the Streamlit app with multiple models.
    """

    def __init__(self):
        self.apps = []

    def run(self):
        """Run the main application."""
        app = SideBar.sidebar()

        if app == "SIR Model":
            SIRModelView().run()
        if app == "SIRS Model":
            SIRSModelView().run()
        if app == "SEIR Model":
            SEIRModelView().run()
        if app == "Home":
            DefaultView().run()
        if app == "About":
            st.title("About")
            st.write("This is a multi-model simulation suite for studying viruses.")

if __name__ == "__main__":
    app = MultiApp()
    app.run()
