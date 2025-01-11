from src.back.agents.BaseAgent import BaseAgent, State


class SEIRAgent(BaseAgent):
    """Modelo SEIR."""
    def __init__(self, *args, exposure_to_infection_chance: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.exposure_to_infection_chance = exposure_to_infection_chance

    def _infection_state(self) -> State:
        return State.EXPOSED

    def _additional_steps(self):
        if self.state == State.EXPOSED:
            self._check_exposure()

    def _check_exposure(self):
        """Si está expuesto, con cierta probabilidad pasa a infectado."""
        if self.random.random() < self.exposure_to_infection_chance:
            self._set_state(State.INFECTED)
