import streamlit as st
from PIL import Image
from pathlib import Path

class DefaultView:
    _PROJECT_PATH = str(Path.cwd())

    """
    Default view that explains the SIR models and their themes.
    """

    def run(self):
        # Título de la página
        st.title("Epidemiological Modeling with SIR Variants 🦠")

        # Subtítulo introductorio
        st.subheader("Understanding SIR, SIRS, and SEIR Models")
        st.write("""
        Epidemiological models are tools to understand and simulate the spread of infectious diseases 
        within a population. Here, we explore three key models and their dynamics:
        """)

        # Cargar la imagen del archivo
        image_path = self._PROJECT_PATH + "/src/webapp/assets/sir.png"  # Ruta de la imagen proporcionada
        st.markdown(
            f"""
                        <div style="text-align: center;">
                            <img src="data:image/png;base64,{self.image_to_base64(image_path)}" alt="Transitions in SIR,
                             SIRS, and SEIR models" style="width: 50%; max-width: 500px; height: auto;">
                            <p><em>Transitions in SIR, SIRS, and SEIR models</em></p>
                        </div>
                        """,
            unsafe_allow_html=True,
        )

        # Explicación de los modelos
        st.write("### 1. SIR Model")
        st.write("""
        The **SIR model** divides the population into three compartments:
        - **S (Susceptible):** Individuals who can become infected.
        - **I (Infected):** Individuals currently infected and contagious.
        - **R (Recovered):** Individuals who have recovered and gained immunity.

        Transitions:
        - Susceptible → Infected: Transmission through contact with an infected individual.
        - Infected → Recovered: Recovery or removal from the infectious state.
        """)

        st.write("### 2. SIRS Model")
        st.write("""
        The **SIRS model** introduces a key change: immunity is temporary.
        - **R (Recovered):** Individuals can lose immunity and return to the susceptible state.

        Transitions:
        - Recovered → Susceptible: Immunity wanes over time.
        """)

        st.write("### 3. SEIR Model")
        st.write("""
        The **SEIR model** adds a new compartment:
        - **E (Exposed):** Individuals who have been infected but are not yet contagious.

        This models diseases with an incubation period. Transitions include:
        - Susceptible → Exposed: Infection occurs, but individuals are not yet infectious.
        - Exposed → Infected: After incubation, individuals become infectious.
        """)

        # Nota final
        st.write("""
        Each model provides a unique perspective on disease dynamics, 
        helping us understand real-world scenarios more effectively.
        """)

    @staticmethod
    def image_to_base64(image_path):
        """Convierte una imagen a base64 para incrustarla en HTML."""
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

# Ejecutar la vista
if __name__ == "__main__":
    DefaultView().run()
