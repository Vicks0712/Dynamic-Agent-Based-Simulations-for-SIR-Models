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
        vaccination_strategy: str = "random",  # Nueva estrategia
        population_structure: str = "erdos_renyi",
        vaccination_chance: float = 0.0,  # Nuevo parámetro
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
        self.seed = seed
        self.vaccination_chance = vaccination_chance
        self.vaccination_strategy = vaccination_strategy
        self.population_structure = population_structure



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

    def should_vaccinate(self) -> bool:
        """Determina si ocurre vacunación en este paso."""
        return self.random.random() < self.vaccination_chance

    @abstractmethod
    def _create_agents(self):
        """Método abstracto para inicializar agentes en el modelo."""
        pass

    def _initialize_network(self):
        graph_generators = {
            "erdos_renyi": lambda: nx.erdos_renyi_graph(
                n=self.num_nodes, p=self.avg_node_degree / self.num_nodes, seed=self.seed
            ),
            "circular": lambda: nx.cycle_graph(self.num_nodes),
        }

        # Verificar si la estructura seleccionada es válida
        if self.population_structure not in graph_generators:
            raise ValueError(
                f"Estructura de población no soportada: {self.population_structure}"
            )

        # Generar el grafo según la estructura seleccionada
        self.G = graph_generators[self.population_structure]()
        self.grid = NetworkGrid(self.G)

    def _initialize_data_collector(self):
        """Configura el recolector de datos."""
        return DataCollector(
            {
                "Susceptible": lambda model: self.number_state(State.SUSCEPTIBLE),
                "Infected": lambda model: self.number_state(State.INFECTED),
                "Recovered": lambda model: self.number_state(State.RECOVERED),
                "Exposed": lambda model: self.number_state(State.EXPOSED),
                "Vaccinated": lambda m: m.number_state(State.VACCINATED),

            }
        )

    def _vaccinate_agents(self):
        """Vacuna a los agentes según la estrategia seleccionada."""
        if self.vaccination_strategy == "Random":
            self._random_vaccination()
        elif self.vaccination_strategy == "Most Popular":
            self._most_popular_vaccination()
        else:
            raise Exception("no va miloko")

    def _random_vaccination(self):
        """Vacuna aleatoriamente a agentes susceptibles."""
        susceptible_agents = [
            agent for agent in self.grid.get_all_cell_contents()
            if agent.state == State.SUSCEPTIBLE or agent.state == State.EXPOSED
        ]

        for agent in susceptible_agents:
            # Con probabilidad "vaccination_chance" se vacuna:
            if self.random.random() < self.vaccination_chance:
                agent._attempt_vaccination()

    def _most_popular_vaccination(self):
        """Vacuna a los agentes susceptibles más conectados."""
        # Ordenar nodos por su grado (popularidad), de mayor a menor
        sorted_nodes = sorted(self.G.degree, key=lambda x: x[1], reverse=True)

        # Obtener los agentes susceptibles en orden de popularidad
        susceptible_agents = [
            agent for node, _ in sorted_nodes
            for agent in self.grid.get_cell_list_contents([node])
            if agent.state == State.SUSCEPTIBLE
        ]

        # Intentar vacunar a cada agente según la probabilidad de vacunación
        for agent in susceptible_agents:
            if self.random.random() < self.vaccination_chance:
                agent._attempt_vaccination()

    def number_state(self, state: State) -> int:
        """Cuenta el número de agentes en un estado específico."""
        return sum(1 for agent in self.grid.get_all_cell_contents() if agent.state == state)




