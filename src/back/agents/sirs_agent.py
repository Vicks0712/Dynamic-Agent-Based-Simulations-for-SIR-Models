from src.back.agents.BaseAgent import BaseAgent, State


class SIRSAgent(BaseAgent):
    """Modelo SIRSV."""
    def __init__(self, *args, immunity_loss_chance: float, vaccine_loss_chance: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.immunity_loss_chance = immunity_loss_chance
        self.vaccine_loss_chance = vaccine_loss_chance

    def _infection_state(self) -> State:
        return State.INFECTED

    def _additional_steps(self):
        """Chequeamos la pérdida de inmunidad si está en R."""
        if self.state == State.RECOVERED:
            self._check_immunity_loss()
        if self.state == State.VACCINED:
            self._check_vaccine_loss()
            

    def _check_immunity_loss(self):
        """Si pierde la inmunidad, pasa de R a S."""
        if self.random.random() < self.immunity_loss_chance:
            self._set_state(State.SUSCEPTIBLE)

    def _check_vaccine_loss(self):
        if self.random.random() < self.vaccine_loss_chance:
            self._set_state(State.SUSCEPTIBLE)
        