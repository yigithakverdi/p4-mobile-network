Sure! Below is the content for `design.md` with detailed topology information for your project.

---

# Design Document

## Introduction

This design document provides a detailed overview of the **SDN and P4 Integrated Mobile Network Simulation** project. It outlines the network topology, describes the components involved, and explains the design decisions made to achieve the project's objectives.

The project integrates two advanced networking concepts:

1. **SDN-Controlled Mobile Network**: An SDN controller manages host tracking, topology discovery, user mobility management, and a fake gateway for ARP handling in a simulated mobile network environment.

2. **P4-Based Distributed Consensus Mechanism**: P4 programmable switches implement a distributed consensus service where each network node votes on packet treatment (allow, drop, abstain), and the final decision is made based on the majority vote.

By combining these concepts, the project aims to demonstrate how programmable data planes and flexible control planes can work together to enhance network performance and adaptability.

---

## Network Topology

### Overview

The network topology simulates a mobile network infrastructure consisting of:

- **User Equipment (UE)**: Mobile devices that connect to the network via access points.
- **Access Points (APs)**: Provide wireless connectivity to UEs.
- **Switches (SW)**: P4 programmable switches that forward traffic and participate in the consensus mechanism.
- **Router (R1)**: Connects the internal network to external networks (e.g., the Internet).
- **SDN Controller**: Manages network functions and controls the switches via OpenFlow.
- **Collision Domains**: Simulate broadcast domains in the network.

### Topology Diagram

Below is a representation of the network topology, illustrating the interconnections between various components such as UEs, APs, switches, and the SDN controller:

<p align="center">
  <img src="/docs/images/topology.png" alt="Network Topology Diagram" width="600"/>
  <br>
  <em>Figure 1: Network Topology Diagram</em>
</p>

### Topology Description

- **User Equipment (UE)**:
  - **UE1**, **UE2**: Mobile devices (e.g., smartphones, laptops) that connect to the network via APs. They can move between APs, simulating user mobility.
- **Access Points (AP)**:
  - **AP1**, **AP2**: Provide wireless connectivity to UEs. Each AP is connected to an edge switch.
- **Switches (SW)**:
  - **SW1**, **SW2**: Edge switches connected to APs. They are P4 programmable switches participating in the consensus mechanism.
  - **SW3**: Core switch connecting edge switches to the router. Also a P4 programmable switch.
- **Router (R1)**:
  - Connects the internal network to external networks (e.g., the Internet). Routes traffic to and from the network.
- **SDN Controller**:
  - Manages all switches via the OpenFlow protocol. Controls network functions such as host tracking, topology discovery, user mobility management, and ARP handling.
- **Collision Domains**:
  - Simulate shared media environments, affecting how packets are transmitted and received in the network.

---

## Module Descriptions

### 1. Host Tracking

**Purpose**: Monitors the location of UEs within the network as they connect to different APs.

**Functionality**:

- Maintains a mapping of UE MAC addresses to their current APs and associated switches.
- Updates flow entries to ensure correct packet forwarding to mobile UEs.
- Detects when a UE moves to a different AP and triggers necessary updates.

### 2. Topology Discovery

**Purpose**: Discovers and maintains an up-to-date view of the network topology.

**Functionality**:

- Uses Link Layer Discovery Protocol (LLDP) packets to detect network devices and links.
- Builds a graph representation of the network using NetworkX library for path computation.
- Updates the topology graph in response to network changes (e.g., link failures, device additions).

### 3. User Mobility Management

**Purpose**: Handles user mobility events and updates network paths accordingly.

**Functionality**:

- Detects when a UE changes its point of attachment (i.e., connects to a different AP).
- Recomputes optimal paths for traffic to and from the UE, aiming to minimize the number of switches that need reconfiguration.
- Installs new flow entries on affected switches to redirect traffic along the new path.
- Ensures minimal disruption and latency during handovers.

### 4. Fake Gateway

**Purpose**: Handles Address Resolution Protocol (ARP) requests for the default gateway to reduce latency and overhead.

**Functionality**:

- Responds to ARP requests directed to the gateway IP with a predefined MAC address.
- Eliminates the need for an actual gateway device to handle ARP requests.
- Reduces broadcast traffic and improves network efficiency.

### 5. Consensus Handler

**Purpose**: Implements the distributed consensus mechanism across P4 programmable switches.

**Functionality**:

- Collects votes from switches embedded in packet headers as packets traverse the network.
- Each switch inspects specific packet fields and votes to allow, drop, or abstain.
- Aggregates votes and determines packet treatment based on the majority decision.
- Final decision is enforced at the egress node or by the controller, ensuring compliance with network policies.

---

## Design Decisions

### Use of P4 Programmable Switches

- **Rationale**: P4 allows for custom packet processing logic directly in the data plane, enabling the implementation of the voting mechanism without additional hardware.
- **Benefits**:
  - Flexibility to define custom headers and processing pipelines.
  - Improved performance by offloading tasks from the control plane to the data plane.
  - Ability to update switch behavior through P4 program modifications.

### Integration with an SDN Controller

- **Rationale**: An SDN controller provides centralized management and control over the network, facilitating dynamic updates and policy enforcement.
- **Benefits**:
  - Simplifies network management and reduces complexity.
  - Enables rapid response to mobility events and topology changes.
  - Central point for implementing network-wide policies and optimizations.

### Minimizing Handover Time

- **Strategy**: When a UE moves to a new AP, the controller computes a new path that requires the least number of switches to be reconfigured.
- **Benefits**:
  - Reduces latency and packet loss during handovers.
  - Improves the user experience by providing seamless connectivity.
  - Decreases the computational overhead on the controller and switches.

### Implementation of the Consensus Mechanism

- **Approach**: Embedding votes within packet headers as they pass through P4 switches.
- **Benefits**:
  - Distributed decision-making improves network resilience.
  - Enhances security by involving multiple nodes in packet treatment decisions.
  - Reduces the risk of single points of failure or compromise.

---

## Data Flow

### Packet Processing Flow

1. **UE Sends Packet**:
   - A UE generates a packet destined for another UE or an external network.
   - The packet is sent to the connected AP.

2. **AP Forwards Packet to Edge Switch**:
   - The AP forwards the packet over a wired connection to its associated edge switch (SW1 or SW2).

3. **Edge Switch Processing**:
   - The edge switch inspects the packet and makes an initial vote based on predefined criteria.
   - The switch embeds its vote into a custom header in the packet.
   - The packet is forwarded towards the destination through the network.

4. **Intermediate Switches**:
   - As the packet traverses intermediate switches (e.g., SW3), each switch inspects the packet.
   - Each switch adds its vote to the custom header without altering previous votes.
   - The packet accumulates votes as it moves through the network.

5. **Egress Switch or Controller Decision**:
   - At the egress switch or upon reaching the destination, the collected votes are evaluated.
   - The decision to allow or drop the packet is made based on the majority of votes.
   - If allowed, the packet proceeds to the destination; otherwise, it is dropped.

6. **SDN Controller Interaction**:
   - The controller may update flow rules based on observed traffic patterns or policy changes.
   - In case of mobility events, the controller recalculates paths and updates switches accordingly.

### ARP Request Handling (Fake Gateway)

1. **UE Sends ARP Request**:
   - A UE broadcasts an ARP request for the gateway IP address.

2. **Edge Switch Captures ARP Request**:
   - The switch matches the ARP request and forwards it to the controller or handles it directly.

3. **Fake Gateway Responds**:
   - The fake gateway module generates an ARP reply with the predefined gateway MAC address.
   - The ARP reply is sent back to the UE, completing the address resolution.

---

## Sequence Diagrams

### User Mobility Event

```plaintext
UE1 -> AP1 -> SW1 -> SDN Controller: UE1 connected to AP1 via SW1
SDN Controller -> SW1: Install flow entries for UE1
UE1 - - - > Moves to AP2
UE1 -> AP2 -> SW2 -> SDN Controller: UE1 connected to AP2 via SW2
SDN Controller -> SW1: Remove flow entries for UE1
SDN Controller -> SW2: Install flow entries for UE1
```

*Figure 2: Sequence Diagram for User Mobility Event*

### Packet Consensus Processing

```plaintext
UE1 -> SW1: Sends packet
SW1: Inspects packet, votes "allow"
SW1 -> SW3: Forwards packet with vote
SW3: Inspects packet, votes "allow"
SW3 -> R1: Forwards packet with accumulated votes
R1: Evaluates votes, decision to "allow"
R1 -> Internet: Forwards packet
```

*Figure 3: Sequence Diagram for Packet Consensus Processing*

---

## Assumptions and Limitations

### Assumptions

- **Homogeneous Switch Capabilities**: All switches in the network support P4 programmability and the required features for the consensus mechanism.
- **Reliable Control Channel**: The SDN controller maintains reliable communication with all switches.
- **Stable Topology**: The physical network topology remains stable during simulation, aside from user mobility events.

### Limitations

- **Scalability**: The centralized SDN controller may become a bottleneck in larger networks.
- **Performance Overhead**: Embedding and processing votes in packet headers introduces additional overhead.
- **Simulation Environment**: The Kathara simulation may not capture all real-world networking nuances, such as wireless interference or physical layer issues.
- **Security Considerations**: The consensus mechanism relies on the integrity of votes; malicious nodes could potentially disrupt the network if not properly secured.

---

## Conclusion

The SDN and P4 Integrated Mobile Network Simulation demonstrates the powerful combination of software-defined networking and programmable data planes. By leveraging P4 switches and an SDN controller, the network can dynamically adapt to user mobility, enforce complex policies through a distributed consensus mechanism, and optimize resource utilization.

This project serves as a foundation for exploring advanced networking concepts and can be extended to include additional features such as enhanced security mechanisms, quality of service (QoS) policies, and integration with other network technologies.

---
