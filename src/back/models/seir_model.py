from src.back.agents.BaseAgent import State
from src.back.agents.seir_agent import SEIRAgent
from src.back.models.BaseModel import BaseModel


class SEIRModel(BaseModel):
    """Modelo SEIR."""
    def __init__(self, *args, exposure_to_infection_chance: float = 0.3,
                 initial_exposed_size: int = 1, initial_infected_size: int = 1, **kwargs):
        self.exposure_to_infection_chance = exposure_to_infection_chance
        self.initial_exposed_size = min(initial_exposed_size, kwargs.get('num_nodes', 10))
        self.initial_infected_size = min(initial_infected_size, kwargs.get('num_nodes', 10))
        super().__init__(*args, **kwargs)

    def _create_agents(self):
        """Crear y asignar agentes al modelo."""
        for node in self.G.nodes():
            agent = SEIRAgent(
                model=self,
                initial_state=State.SUSCEPTIBLE,
                virus_spread_chance=self.virus_spread_chance,
                virus_check_frequency=self.virus_check_frequency,
                exposure_to_infection_chance=self.exposure_to_infection_chance,
                recovery_chance=self.recovery_chance,
                gain_resistance_chance=self.gain_resistance_chance,
                seed=self.seed,
                vaccination_chance=self.vaccination_chance

            )
            self.grid.place_agent(agent, node)

        # Exponer nodos iniciales
        exposed_nodes = self.random.sample(list(self.G), self.initial_exposed_size)
        for agent in self.grid.get_cell_list_contents(exposed_nodes):
            agent.state = State.EXPOSED

        # Infectar nodos iniciales
        # Aseguramos que los infectados no se solapen con los expuestos
        remaining_nodes = list(set(self.G.nodes) - set(exposed_nodes))
        infected_nodes = self.random.sample(remaining_nodes, self.initial_infected_size)
        for agent in self.grid.get_cell_list_contents(infected_nodes):
            agent.state = State.INFECTED
