from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu


class SideBar:
    """
    A class to create and manage the sidebar for the Streamlit application.

    This class handles the setup of the sidebar, including a navigation menu with options for different sections of the application.
    """
    _PROJECT_PATH = str(Path.cwd())


    @staticmethod
    def sidebar():
        with st.sidebar:
            st.image(SideBar._PROJECT_PATH + "/src/webapp/assets/siani.png", use_container_width=True)
            app = option_menu(
                menu_title="Menu",
                options=[ "Home","SIR Model", "SIRS Model", "SEIR Model"],
                icons=["house-fill", "virus", "virus", "virus"],
                menu_icon="menu-button-wide-fill",
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#f7f7f7"},  # Fondo gris claro
                    "icon": {"color": "#6c757d", "font-size": "18px"},  # Gris suave para los íconos
                    "nav-link": {
                        "color": "#495057",  # Texto gris medio
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "5px",
                        "--hover-color": "#e9ecef",  # Fondo gris más claro al pasar el cursor
                    },
                    "nav-link-selected": {
                        "background-color": "#dee2e6",  # Fondo gris claro para la opción seleccionada
                        "color": "#212529",  # Texto gris oscuro
                        "font-weight": "bold",
                    },
                },
            )
        return app