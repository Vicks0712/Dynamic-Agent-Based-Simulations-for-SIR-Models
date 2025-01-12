# Agent-Based Epidemiological Models Simulator
[![My Skills](https://skillicons.dev/icons?i=python,github)](https://skillicons.dev)
<img src="https://raw.githubusercontent.com/projectmesa/mesa/main/docs/images/mesa_logo.png" alt="Mesa Logo" width="50" style="margin-left: 5px">
<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit Logo" width="50" style="margin-left: 5px">


This project implements a simulator for epidemiological models using agent-based programming. It allows the analysis of infectious disease dynamics under various scenarios, such as immunity loss, incubation periods, and vaccination strategies.


## Table of Contents

1. [Included Models](#included-models)
2. [Usage](#usage)
    - [Execution](#execution)
    - [Parameter Configuration](#parameter-configuration)
    - [Visualization](#visualization)
3. [Features](#features)
4. [System Requirements](#system-requirements)
5. [Project Structure](#project-structure)




## Included Models

The simulator supports the following models:

1. **SIR(V):** Classic spread model with vaccination.
2. **SIRS:** Includes immunity loss, with and without vaccination.
3. **SEIR(V):** Considers an incubation period before active infection, with targeted or random vaccination strategies.

Each model is highly configurable and allows adjustment of parameters such as transmission rates, recovery rates, immunity loss, and vaccination strategies.


## Usage

### Execution

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Run the interactive interface:
```bash
streamlit run app.py
```

### Parameter Configuration

The interface allows configuration of parameters such as:
- **Population size:** Number of nodes in the network.
- **Average connections:** Contacts per node.
- **Transmission, recovery, and immunity loss rates.**
- **Vaccination strategies.**
- **Simulation duration (in days).**

### Visualization

The simulation generates graphs showing:
- Temporal evolution of states (\( S, E, I, R, V \)).
- Population network with nodes colored by their state.


![image](https://github.com/user-attachments/assets/5c00588a-6b80-4fba-ae87-cec7d65a53f8)


## Features

- Agent-based simulation using the `Mesa` library.
- Support for different population network structures:
  - **Erdős–Rényi**
  - **Circular**
  - **Kamada-Kawai**
- Vaccination strategies:
  - **Random:** Vaccination of randomly selected nodes.
  - **Most Popular:** Targeted vaccination of the most connected nodes.
- Real-time data collection and result visualization.



## System Requirements

- Python 3.8+
- Required libraries:
  - `mesa`
  - `matplotlib`
  - `networkx`
  - `streamlit`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── src
│   ├── back
│   │   ├── agents
│   │   │   ├── BaseAgent.py
│   │   │   ├── SIRAgent.py
│   │   │   ├── SIRSAgent.py
│   │   │   └── SEIRAgent.py
│   │   ├── models
│   │   │   ├── BaseModel.py
│   │   │   ├── SIRModel.py
│   │   │   ├── SIRSModel.py
│   │   │   └── SEIRModel.py
│   ├── webapp
│   │   ├── views
│   │   │   └── SimulationView.py
│   ├── utils
│       └── GraphUtils.py
├── app.py
├── requirements.txt
└── README.md
```


