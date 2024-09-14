# main.py
import os
import yaml
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls

from host_tracking import HostTracking
from topology_discovery import TopologyDiscovery
from user_mobility import UserMobility
from fake_gateway import FakeGateway
from consensus_handler import ConsensusHandler

class MainController(app_manager.RyuApp):
    OFP_VERSIONS = [1.3]

    def __init__(self, *args, **kwargs):
        # Initialize the MainController and its components
        super(MainController, self).__init__(*args, **kwargs)
        self.logger.setLevel(logging.DEBUG)
        self.host_tracking = HostTracking(self)
        self.topology_discovery = TopologyDiscovery(self)
        self.user_mobility = UserMobility(self)
        self.fake_gateway = FakeGateway(self)
        self.consensus_handler = ConsensusHandler(self)

    def __init__(self, *args, **kwargs):
        super(MainController, self).__init__(*args, **kwargs)

        # Load configurations from controller-config.yaml
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'controller-config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Set OpenFlow versions from configuration
        self.OFP_VERSIONS = self.config.get('controller', {}).get('ofp_versions', [1.3])

        # Initialize modules with configurations
        self.host_tracking = HostTracking(self, self.config)
        self.topology_discovery = TopologyDiscovery(self, self.config)
        self.user_mobility = UserMobility(self, self.config)
        self.fake_gateway = FakeGateway(self, self.config)
        self.consensus_handler = ConsensusHandler(self, self.config)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, MAIN_DISPATCHER)
    def switch_features_handler(self, ev):
        # Handle switch feature events
        # Add the switch to topology discovery and set up fake gateway flows
        datapath = ev.msg.datapath
        self.topology_discovery.add_switch(datapath)
        self.fake_gateway.add_flow(datapath)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        # Handle packet-in events
        # Process packets for host tracking and user mobility
        msg = ev.msg
        datapath = msg.datapath
        self.logger.debug(f"Packet in from datapath: {datapath.id}")
        self.host_tracking.handle_packet_in(msg)
        self.user_mobility.handle_packet_in(msg)

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self, ev):
        # Handle port status change events
        # Log port status changes and update topology discovery
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        if msg.reason == ofp.OFPPR_ADD:
            reason = 'ADD'
        elif msg.reason == ofp.OFPPR_DELETE:
            reason = 'DELETE'
        elif msg.reason == ofp.OFPPR_MODIFY:
            reason = 'MODIFY'
        else:
            reason = 'unknown'
        self.logger.info(f'Port {msg.desc.port_no} on switch {datapath.id} {reason}')
        self.topology_discovery.update_port_status(datapath, msg.desc, reason)

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        # Handle flow removed events
        # Log details about removed flows
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        if msg.reason == ofp.OFPRR_IDLE_TIMEOUT:
            reason = 'IDLE TIMEOUT'
        elif msg.reason == ofp.OFPRR_HARD_TIMEOUT:
            reason = 'HARD TIMEOUT'
        elif msg.reason == ofp.OFPRR_DELETE:
            reason = 'DELETE'
        elif msg.reason == ofp.OFPRR_GROUP_DELETE:
            reason = 'GROUP DELETE'
        else:
            reason = 'unknown'
        self.logger.info(f'Flow removed: reason={reason}, priority={msg.priority}, '
                         f'cookie={msg.cookie}, table_id={msg.table_id}')
