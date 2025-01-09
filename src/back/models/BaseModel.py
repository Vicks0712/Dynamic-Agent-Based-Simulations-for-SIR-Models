from mesa import Model
from mesa.space import NetworkGrid
import networkx as nx
from mesa.datacollection import DataCollector
from abc import ABC, abstractmethod

from src.back.agents.BaseAgent import State

class BaseModel(Model, ABC):
    """Clase base para modelos epidemiológicos."""

    def __init__(
        self,
        num_nodes: int,
        avg_node_degree: int,
        virus_spread_chance: float,
        virus_check_frequency: float,
        recovery_chance: float,
        gain_resistance_chance: float,
        vaccination_rate: float,
        vaccination_effectiveness: float,
        vaccination_strategy: str = "Random",
        seed: int = None,
        **kwargs,  # Captura argumentos adicionales
    ):
        super().__init__(seed=seed)
        self.num_nodes = num_nodes
        self.avg_node_degree = avg_node_degree
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        self.vaccination_rate = vaccination_rate
        self.vaccination_effectiveness = vaccination_effectiveness
        self.vaccination_strategy = vaccination_strategy

        # Inicializar red y agentes
        self._initialize_network()
        self._create_agents()

        # Recolector de datos
        self.datacollector = self._initialize_data_collector()
        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """Avanza la simulación un paso de tiempo."""
        self._vaccinate_agents()
        for agent in self.grid.get_all_cell_contents():
            agent.step()
        self.datacollector.collect(self)

    @abstractmethod
    def _create_agents(self):
        """Método abstracto para inicializar agentes en el modelo."""
        pass

    def _initialize_network(self):
        """Crea la red de nodos y la grilla."""
        prob = self.avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = NetworkGrid(self.G)

    def _vaccinate_agents(self):
        """Vacuna a los agentes según la estrategia seleccionada."""
        if self.vaccination_strategy == "Random":
            self._random_vaccination()
        elif self.vaccination_strategy == "Most Popular":
            self._most_popular_vaccination()

    def _random_vaccination(self):
        """Vacuna aleatoriamente a agentes susceptibles."""
        susceptible_agents = [
            agent for agent in self.grid.get_all_cell_contents() if agent.state == State.SUSCEPTIBLE
        ]
        num_to_vaccinate = int(len(susceptible_agents) * self.vaccination_rate)
        agents_to_vaccinate = self.random.sample(susceptible_agents, num_to_vaccinate)
        for agent in agents_to_vaccinate:
            agent._attempt_vaccination()

    def _most_popular_vaccination(self):
        """Vacuna a los agentes susceptibles más conectados."""
        sorted_nodes = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        susceptible_agents = [
            agent for node, _ in sorted_nodes
            for agent in self.grid.get_cell_list_contents([node])
            if agent.state == State.SUSCEPTIBLE
        ]
        num_to_vaccinate = int(len(susceptible_agents) * self.vaccination_rate)
        for agent in susceptible_agents[:num_to_vaccinate]:
            agent._attempt_vaccination()

    def _initialize_data_collector(self):
        """Configura el recolector de datos."""
        return DataCollector(
            {
                "Susceptible": lambda model: self.number_state(State.SUSCEPTIBLE),
                "Infected": lambda model: self.number_state(State.INFECTED),
                "Exposed": lambda model: self.number_state(State.EXPOSED),  # Añadido
                "Resistant": lambda model: self.number_state(State.RECOVERED),
                "Vaccinated": lambda model: self.number_state(State.VACCINATED),
            }
        )

    def number_state(self, state: State) -> int:
        """Cuenta el número de agentes en un estado específico."""
        return sum(1 for agent in self.grid.get_all_cell_contents() if agent.state == state)

    def should_vaccinate(self) -> bool:
        """Determina si ocurre vacunación en este paso."""
        return self.random.random() < self.vaccination_rate
