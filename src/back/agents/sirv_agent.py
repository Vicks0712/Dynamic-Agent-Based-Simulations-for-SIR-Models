from src.back.agents.BaseAgent import BaseAgent, State


class SIRVAgent(BaseAgent):
    """Modelo SIRV."""
    def _infection_state(self) -> State:
        return State.INFECTED  # Estado por defecto al infectar vecinos

    def _additional_steps(self):
        pass  # SIRV no necesita lógica adicional
