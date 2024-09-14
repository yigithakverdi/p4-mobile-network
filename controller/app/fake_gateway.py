from ryu.lib.packet import packet, ethernet, arp
from ryu.ofproto import ether

class FakeGateway:
    def __init__(self, main_app, config):
        self.main_app = main_app
        self.config = config
        controller_config = config.get('controller', {})
        self.gateway_ip = controller_config.get('gateway_ip', '10.0.0.254')
        self.gateway_mac = controller_config.get('gateway_mac', 'aa:bb:cc:dd:ee:ff')

    def add_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_type=ether.ETH_TYPE_ARP, arp_tpa=self.gateway_ip)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.main_app.user_mobility.add_flow(datapath, 1, match, actions)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def arp_handler(self, ev):        
        # Handle incoming ARP requests for the gateway IP
        msg = ev.msg
        datapath = msg.datapath
        pkt = packet.Packet(msg.data)
        arp_pkt = pkt.get_protocol(arp.arp)
        if arp_pkt and arp_pkt.opcode == arp.ARP_REQUEST and arp_pkt.dst_ip == self.gateway_ip:
            self.send_arp_reply(datapath, arp_pkt.src_mac, arp_pkt.src_ip)

    def send_arp_reply(self, datapath, dst_mac, dst_ip):
        # Send an ARP reply from the fake gateway to the requesting host
        e = ethernet.ethernet(dst_mac, self.gateway_mac, ether.ETH_TYPE_ARP)
        a = arp.arp_ip(arp.ARP_REPLY, self.gateway_mac, self.gateway_ip, dst_mac, dst_ip)
        p = packet.Packet()
        p.add_protocol(e)
        p.add_protocol(a)
        p.serialize()
        actions = [datapath.ofproto_parser.OFPActionOutput(ofproto.OFPP_IN_PORT)]
        out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath,
                                                   buffer_id=ofproto.OFP_NO_BUFFER,
                                                   in_port=ofproto.OFPP_CONTROLLER,
                                                   actions=actions,
                                                   data=p.data)
        datapath.send_msg(out)
