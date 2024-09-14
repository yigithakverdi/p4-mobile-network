# consensus_handler.py
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.lib.packet import packet

class ConsensusHandler:
    def __init__(self, main_app, config):
        self.main_app = main_app
        self.config = config
        controller_config = config.get('controller', {})
        self.required_votes_percentage = controller_config.get('required_votes_percentage', 51)
        self.votes = {}

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def consensus_packet_in(self, ev):
        # Extract votes from packet metadata or headers
        msg = ev.msg
        datapath = msg.datapath
        pkt = packet.Packet(msg.data)

        # Assume custom header contains votes
        # For this example, we will use a dummy method to extract votes
        vote = self.extract_vote(pkt)
        packet_id = self.get_packet_id(pkt)

        if packet_id not in self.votes:
            self.votes[packet_id] = []
        self.votes[packet_id].append(vote)
        
        # Take action based on consensus
        if self.is_majority_reached(self.votes[packet_id]):
            if self.should_forward(self.votes[packet_id]):
                self.forward_packet(msg)
            else:
                pass
            del self.votes[packet_id]

    # Extract vote from custom header
    def extract_vote(self, pkt):
        for protocol in pkt.protocols:
            if hasattr(protocol, 'vote_value'):
                vote_value = protocol.vote_value
                if vote_value == 1:
                    return 'allow'
                elif vote_value == 2:
                    return 'drop'
                else:
                    return 'abstain'
        return 'abstain'

    # Generate a unique identifier for the packet
    def get_packet_id(self, pkt):
        return hash(pkt)
    # Determine if the majority has been reached
    def is_majority_reached(self, votes):        
        return len(votes) >= self.required_votes()

    # Define the number of votes required for a decision
    # For example, absolute majority of the nodes
    def required_votes(self):
        # Calculate required votes based on the percentage
        total_nodes = len(self.main_app.topology_discovery.datapaths)
        required_votes = int((self.required_votes_percentage / 100.0) * total_nodes)
        return max(1, required_votes)  # Ensure at least one vote is required
    
    # Decide whether to forward or drop the packet based on votes
    def should_forward(self, votes):        
        allowed = votes.count('allow')
        dropped = votes.count('drop')
        if allowed > dropped:
            return True
        else:
            return False

    # Forward the packet to its destination
    def forward_packet(self, msg):
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(ofproto.OFPP_TABLE)]
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=msg.match['in_port'],
                                  actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
