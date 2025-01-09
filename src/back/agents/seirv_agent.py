from src.back.agents.BaseAgent import BaseAgent, State


class SEIRVAgent(BaseAgent):
    """Modelo SEIRV."""
    def __init__(self, *args, exposure_to_infection_chance: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.exposure_to_infection_chance = exposure_to_infection_chance

    def _infection_state(self) -> State:
        return State.EXPOSED

    def _additional_steps(self):
        if self.state == State.EXPOSED:
            self._check_exposure()

    def _check_exposure(self):
        """Chequea si un agente expuesto pasa a estar infectado."""
        if self.random.random() < self.exposure_to_infection_chance:
            self._set_state(State.INFECTED)