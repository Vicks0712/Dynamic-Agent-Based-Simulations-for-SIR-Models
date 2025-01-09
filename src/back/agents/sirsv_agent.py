from src.back.agents.BaseAgent import BaseAgent, State


class SIRSVAgent(BaseAgent):
    """Modelo SIRSV."""
    def __init__(self, *args, immunity_loss_chance: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.immunity_loss_chance = immunity_loss_chance

    def _infection_state(self) -> State:
        return State.INFECTED

    def _additional_steps(self):
        if self.state == State.RECOVERED:
            self._check_immunity_loss()

    def _check_immunity_loss(self):
        """Chequea si un agente pierde su inmunidad."""
        if self.random.random() < self.immunity_loss_chance:
            self._set_state(State.SUSCEPTIBLE)