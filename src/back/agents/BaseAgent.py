from mesa import Agent
from enum import Enum
from abc import ABC, abstractmethod


class State(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    VACCINATED = 3
    EXPOSED = 4  # Opcional, usado en SEIRV y similares


class BaseAgent(Agent, ABC):
    """Clase base para agentes de modelos de transmisión de virus."""

    def __init__(
            self,
            model,
            initial_state: State,
            virus_spread_chance: float,
            virus_check_frequency: float,
            recovery_chance: float,
            gain_resistance_chance: float,
            vaccination_effectiveness: float,
    ):
        super().__init__(model)
        self.state = initial_state
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.vaccination_effectiveness = vaccination_effectiveness

    def step(self):
        """Lógica común para todos los agentes."""
        if self.state == State.INFECTED:
            self._infect_neighbors()
        elif self.state == State.SUSCEPTIBLE and self.model.should_vaccinate():
            self._attempt_vaccination()
        self._check_health_status()
        self._additional_steps()  # Método para lógica específica

    @abstractmethod
    def _additional_steps(self):
        """Método abstracto para implementar lógica específica en subclases."""
        pass

    def _infect_neighbors(self):
        """Intenta infectar a los vecinos susceptibles."""
        neighbors = self._get_neighbors()
        for neighbor in neighbors:
            if neighbor.state == State.SUSCEPTIBLE and self._should_infect():
                neighbor._set_state(self._infection_state())

    @abstractmethod
    def _infection_state(self) -> State:
        """Devuelve el estado al que los vecinos son infectados (por defecto INFECTED)."""
        return State.INFECTED

    def _check_health_status(self):
        """Chequea el estado de salud del agente."""
        if self.state == State.INFECTED and self._should_check_status():
            self._attempt_recovery()

    def _attempt_recovery(self):
        """Intenta recuperarse o ganar resistencia."""
        if self._should_recover():
            self._set_state(State.SUSCEPTIBLE)
            if self._should_gain_resistance():
                self._set_state(State.RECOVERED)

    def _attempt_vaccination(self):
        """Intenta vacunar al agente."""
        if self.random.random() < self.vaccination_effectiveness:
            self._set_state(State.VACCINATED)

    def _get_neighbors(self):
        """Obtiene vecinos susceptibles."""
        neighbors_nodes = self.model.grid.get_neighborhood(self.pos, include_center=False)
        return [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state == State.SUSCEPTIBLE
        ]

    def _should_infect(self) -> bool:
        """Determina si el agente infecta a un vecino."""
        return self.random.random() < self.virus_spread_chance

    def _should_check_status(self) -> bool:
        """Determina si el agente revisa su estado de infección."""
        return self.random.random() < self.virus_check_frequency

    def _should_recover(self) -> bool:
        """Determina si el agente se recupera de la infección."""
        return self.random.random() < self.recovery_chance

    def _should_gain_resistance(self) -> bool:
        """Determina si el agente gana resistencia."""
        return self.random.random() < self.gain_resistance_chance

    def _set_state(self, new_state: State):
        """Establece el estado del agente."""
        self.state = new_state