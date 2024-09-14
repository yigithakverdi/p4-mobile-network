# user_mobility.py
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.lib.packet import packet, ethernet

class UserMobility:
    def __init__(self, main_app):
        # Initialize the UserMobility class with references to main app and its components
        self.main_app = main_app
        self.host_tracking = main_app.host_tracking
        self.topology_discovery = main_app.topology_discovery


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        # Handle packet-in events to manage user mobility
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        src_mac = eth.src
        dst_mac = eth.dst

        # Learn the location of the source host
        self.host_tracking.learn_host(datapath, src_mac, in_port)

        # Get the location of the destination host
        dst_dpid, dst_port = self.host_tracking.get_host_location(dst_mac)
        if dst_dpid:
            # If destination is known, calculate and install the path
            path = self.topology_discovery.get_shortest_path(datapath.id, dst_dpid)
            if path:
                self.install_path(path, src_mac, dst_mac)
        else:
            # If destination is unknown, do nothing (implicit flooding will occur)
            pass

    def install_path(self, path, src_mac, dst_mac):
        # Install flow rules along the path for the given source and destination
        self.main_app.logger.debug(f"Installing path: {path} for {src_mac} -> {dst_mac}")        
        for i in range(len(path) - 1):
            datapath = self.topology_discovery.datapaths[path[i]]
            out_port = self.topology_discovery.network_graph[path[i]][path[i+1]]['port']
            match = datapath.ofproto_parser.OFPMatch(eth_src=src_mac, eth_dst=dst_mac)
            actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
            self.add_flow(datapath, 1, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        # Helper method to add a flow rule to a datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match,
                                instructions=inst)
        datapath.send_msg(mod)
