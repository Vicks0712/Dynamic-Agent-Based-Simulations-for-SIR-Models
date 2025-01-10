from src.back.agents.BaseAgent import State
from src.back.agents.sirs_agent import SIRSAgent
from src.back.models.BaseModel import BaseModel


class SIRSModel(BaseModel):
    """Modelo SIRS."""
    def __init__(self, *args, immunity_loss_chance: float = 0.1,
                 vaccine_loss_chance: float = 0.01, initial_outbreak_size: int = 1, **kwargs):
        # Configurar atributos específicos antes del constructor de la base
        self.immunity_loss_chance = immunity_loss_chance
        self.initial_outbreak_size = min(initial_outbreak_size, kwargs.get('num_nodes', 10))
        self.vaccine_loss_chance = vaccine_loss_chance
        super().__init__(*args, **kwargs)

    def _create_agents(self):
        """Crear y asignar agentes al modelo."""
        for node in self.G.nodes():
            agent = SIRSAgent(
                model=self,
                initial_state=State.SUSCEPTIBLE,
                virus_spread_chance=self.virus_spread_chance,
                virus_check_frequency=self.virus_check_frequency,
                recovery_chance=self.recovery_chance,
                gain_resistance_chance=self.gain_resistance_chance,
                immunity_loss_chance=self.immunity_loss_chance,
                seed=self.seed,
                vaccination_chance=self.vaccination_chance,
                vaccine_loss_chance=self.vaccine_loss_chance

            )
            self.grid.place_agent(agent, node)

        # Infectar nodos iniciales
        infected_nodes = self.random.sample(list(self.G), self.initial_outbreak_size)
        for agent in self.grid.get_cell_list_contents(infected_nodes):
            agent.state = State.INFECTED
