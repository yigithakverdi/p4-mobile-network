# topology_discovery.py
from ryu.topology import event
from ryu.topology.api import get_switch, get_link
import networkx as nx

class TopologyDiscovery:
    def __init__(self, main_app):
        # Initialize the TopologyDiscovery class with the main application
        # Set up a network graph and a dictionary to store datapaths
        self.main_app = main_app
        self.network_graph = nx.Graph()
        self.datapaths = {}

    def add_switch(self, datapath):
        # Add a switch to the topology
        # Store the datapath object and add a node to the network graph
        dpid = datapath.id
        self.datapaths[dpid] = datapath
        self.network_graph.add_node(dpid)

    def remove_switch(self, datapath):
        # Remove a switch from the topology
        # Delete the datapath object and remove the node from the network graph
        dpid = datapath.id
        del self.datapaths[dpid]
        self.network_graph.remove_node(dpid)

    def add_link(self, src_dpid, dst_dpid, port_no):
        # Add a link between two switches in the network graph
        # The port number is stored as an attribute of the edge
        self.network_graph.add_edge(src_dpid, dst_dpid, port=port_no)

    def get_shortest_path(self, src_dpid, dst_dpid):
        # Calculate the shortest path between two switches
        # Returns the path if it exists, None otherwise
        try:
            return nx.shortest_path(self.network_graph, src_dpid, dst_dpid)
        except nx.NetworkXNoPath:
            return None

    def register_handlers(self):
        # Register event handlers for switch enter and link add events
        self.main_app.register_event(event.EventSwitchEnter, self.switch_enter_handler)
        self.main_app.register_event(event.EventLinkAdd, self.link_add_handler)

    def switch_enter_handler(self, ev):
        # Handle switch enter events
        # Add the new switch to the topology
        switch = ev.switch
        self.add_switch(switch.dp)

    def link_add_handler(self, ev):
        # Handle link add events
        # Add the new link to the topology
        src = ev.link.src
        dst = ev.link.dst
        self.add_link(src.dpid, dst.dpid, src.port_no)
