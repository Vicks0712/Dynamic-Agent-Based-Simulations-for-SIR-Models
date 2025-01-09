import streamlit as st
import time

class Animation:
    @staticmethod
    def run(model, update_data_callback, graph_callbacks, steps):
        for _ in range(steps):
            if not st.session_state.is_playing_sirsv:
                break
            model.step()
            update_data_callback()
            if len(graph_callbacks) > 0:
                graph_callbacks[0]()  # Update network graph
            if len(graph_callbacks) > 1:
                graph_callbacks[1]()  # Update population graph
            time.sleep(0.1)
