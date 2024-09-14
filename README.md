# SDN and P4 Integrated Mobile Network Simulation
This repository hosts an advanced network simulation project that integrates Software-Defined Networking (SDN) and P4 programmable switches to create a realistic mobile network environment. It combines a SDN-controlled mobile network simulation with a P4-based distributed consensus mechanism. The project utilizes Kathara for network device simulation and implements custom P4 programs and SDN controller applications.

## Table of Contents

- [Project Title: SDN and P4 Integrated Mobile Network Simulation](#project-title-sdn-and-p4-integrated-mobile-network-simulation)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Set Up the Python Virtual Environment](#3-set-up-the-python-virtual-environment)
    - [4. Compile P4 Programs](#4-compile-p4-programs)
  - [Running the Simulation](#running-the-simulation)
    - [1. Start the Kathara Lab](#1-start-the-kathara-lab)
    - [2. Start the SDN Controller](#2-start-the-sdn-controller)
  - [Project Components](#project-components)
    - [1. Kathara Lab](#1-kathara-lab)
    - [2. P4 Programs](#2-p4-programs)
    - [3. SDN Controller Applications](#3-sdn-controller-applications)
  - [Usage Guide](#usage-guide)
    - [Simulating User Mobility](#simulating-user-mobility)
    - [Testing the Consensus Mechanism](#testing-the-consensus-mechanism)
  - [Development Guide](#development-guide)
    - [Modifying P4 Programs](#modifying-p4-programs)
    - [Updating Controller Logic](#updating-controller-logic)
    - [Testing and Debugging](#testing-and-debugging)
  - [Troubleshooting](#troubleshooting)

---

## Project Overview

This project merges two networking concepts into a unified simulation environment:

1. **SDN-Controlled Mobile Network**: Simulates a mobile network where an SDN controller manages host tracking, topology discovery, user mobility, and a fake gateway for ARP handling.
2. **P4-Based Distributed Consensus Mechanism**: Implements a distributed consensus service using P4 programmable switches, where each node votes on packet treatment (allow, drop, abstain), and the final decision is made based on the majority vote.

The integrated project uses **Kathara** to simulate network devices and **P4** for programmable switches, providing a platform to study advanced networking concepts in a controlled environment.

---

## Features

- **Host Tracking**: Monitors user devices as they move across the network.
- **Topology Discovery**: Dynamically discovers the network topology.
- **User Mobility Management**: Handles path updates and minimizes reconfiguration during handovers.
- **Fake Gateway**: Responds to ARP requests addressed to the gateway to reduce latency.
- **Distributed Consensus Mechanism**: Implements a voting system across network nodes to decide packet treatment.
- **P4 Programmable Switches**: Uses P4 language for advanced packet processing and custom logic implementation.
- **Kathara Simulation Environment**: Simulates network devices and collision domains.

---

## Project Structure

```
project-root/
├── README.md
├── LICENSE
├── kathara-lab/
│   ├── lab.conf
│   ├── nodes/
│   │   ├── SW1/
│   │   │   ├── startup.sh
│   │   │   └── config/
│   │   │       ├── switch.json
│   │   │       └── runtime.json
│   │   ├── R1/
│   │   │   ├── startup.sh
│   │   │   └── config/
│   │   │       └── router-config.conf
│   │   └── ...
├── controller/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── host_tracking.py
│   │   ├── topology_discovery.py
│   │   ├── user_mobility.py
│   │   ├── fake_gateway.py
│   │   └── consensus_handler.py
│   ├── config/
│   │   └── controller-config.yaml
│   └── requirements.txt
├── p4-programs/
│   ├── switch.p4
│   └── ...
├── scripts/
│   ├── start_lab.sh
│   ├── stop_lab.sh
│   └── ...
├── docs/
│   └── ...
└── tests/
    └── ...
```

---

## Prerequisites

- **Operating System**: Ubuntu 20.04 LTS or compatible
- **Python**: Version 3.6 or higher
- **Kathara**: Network emulation platform
- **P4 Compiler (p4c)**: For compiling P4 programs
- **Docker**: Required by Kathara

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies

**Install Kathara**

Follow the official Kathara installation guide:

```bash
sudo apt-get update
sudo apt-get install -y python3-pip docker.io
pip3 install kathara
```

**Install P4 Compiler**

Follow the instructions from the P4 community:

```bash
# Install dependencies
sudo apt-get install -y git cmake build-essential libgc-dev bison flex libfl-dev libgmp-dev libboost-dev libboost-iostreams-dev libboost-graph-dev llvm pkg-config python3-pip

# Clone the p4c repository
git clone https://github.com/p4lang/p4c.git
cd p4c
mkdir build
cd build
cmake ..
make -j4
sudo make install
```

### 3. Set Up the Python Virtual Environment

```bash
cd controller/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Compile P4 Programs

```bash
cd p4-programs/
p4c --target bmv2 --arch v1model -o switch.json switch.p4
cp switch.json ../kathara-lab/nodes/SW1/config/
```

---

## Running the Simulation

### 1. Start the Kathara Lab

```bash
cd kathara-lab/
kathara lstart
```

### 2. Start the SDN Controller

In a new terminal:

```bash
cd controller/
source venv/bin/activate
ryu-manager app/main.py
```

---

## Project Components

### 1. Kathara Lab

- **`lab.conf`**: Defines the network topology.
- **`nodes/`**: Contains configurations and startup scripts for each network device.
  - **`SW1/`**: P4 programmable switch.
  - **`R1/`**: Router configured with Quagga.
- **`collision-domains/`**: Configuration for collision domains if applicable.

### 2. P4 Programs

- **`switch.p4`**: P4 program for the programmable switch, implementing packet parsing, header manipulation, and the voting mechanism for consensus.

### 3. SDN Controller Applications

- **`main.py`**: Entry point for the SDN controller.
- **`host_tracking.py`**: Tracks hosts and their locations in the network.
- **`topology_discovery.py`**: Discovers and maintains the network topology.
- **`user_mobility.py`**: Manages user mobility and updates flows accordingly.
- **`fake_gateway.py`**: Handles ARP requests to the gateway.
- **`consensus_handler.py`**: Implements the distributed consensus mechanism.
- **`controller-config.yaml`**: Configuration file for the controller.
- **`requirements.txt`**: Lists Python dependencies.

---

## Usage Guide

### Simulating User Mobility

1. **Move a Host**: In the Kathara environment, simulate a host moving by changing its connection point.
2. **Controller Reaction**: The SDN controller detects the change and updates flow entries to reroute traffic.
3. **Minimize Reconfiguration**: The controller aims to minimize the number of devices that need reconfiguration during the handover.

### Testing the Consensus Mechanism

1. **Generate Traffic**: Send packets through the network that require consensus-based decision-making.
2. **Voting Process**: Each P4 switch votes on the packet's treatment based on its inspection.
3. **Final Decision**: The egress node or controller makes the final decision to forward or drop the packet based on the majority vote.

---

## Development Guide

### Modifying P4 Programs

1. **Edit P4 Code**: Make changes to `p4-programs/switch.p4` as needed.
2. **Compile the Program**:

   ```bash
   cd p4-programs/
   p4c --target bmv2 --arch v1model -o switch.json switch.p4
   cp switch.json ../kathara-lab/nodes/SW1/config/
   ```

3. **Restart the Switch Node**:

   ```bash
   kathara stop SW1
   kathara start SW1
   ```

### Updating Controller Logic

1. **Edit Controller Code**: Modify the relevant Python files in `controller/app/`.
2. **Restart the Controller**:

   ```bash
   cd controller/
   source venv/bin/activate
   ryu-manager app/main.py
   ```

### Testing and Debugging

- **Logging**: Use logging statements in your controller applications to trace execution.
- **Packet Sniffing**: Use tools like Wireshark or `tcpdump` within Kathara nodes to inspect traffic.
- **Unit Tests**: Write unit tests for controller modules.
- **Integration Tests**: Simulate complex scenarios to test the integrated system.

---

## Troubleshooting

- **Controller Not Connecting to Switches**: Ensure that the controller and switches are configured to use the same OpenFlow version and that the controller's IP and port are correctly specified.
- **P4 Program Compilation Errors**: Check the P4 code for syntax errors and ensure that all required headers and metadata are defined.
- **Kathara Lab Issues**: Verify that Docker is running and that Kathara is properly installed. Use `kathara lclean` to clean up and restart the lab if necessary.
- **Permission Errors**: Some operations may require root privileges. Use `sudo` where appropriate.
