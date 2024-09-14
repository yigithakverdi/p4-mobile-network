from ryu.base import app_manager
from ryu.controller import mac_to_port

class HostTracking:
    def __init__(self, main_app, config):
        self.main_app = main_app
        self.config = config
        self.mac_to_port = {}

    def learn_host(self, datapath, src_mac, in_port):
        # Learn the location of a host by associating its MAC address
        # with the input port on a specific datapath (switch)
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src_mac] = in_port

    def get_host_location(self, src_mac):
        # Retrieve the location (datapath ID and port) of a host
        # given its MAC address
        for dpid in self.mac_to_port:
            if src_mac in self.mac_to_port[dpid]:
                return dpid, self.mac_to_port[dpid][src_mac]
        return None, None
