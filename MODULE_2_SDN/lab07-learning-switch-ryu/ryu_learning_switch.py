from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class RyuLearningSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RyuLearningSwitch, self).__init__(*args, **kwargs)
        # mac_to_port[dpid][mac_address] = port
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {})

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src
        
        # Ignores IPv6 multicast for clean console logs
        if eth.ethertype == 34525: 
            return

        self.logger.info("packet in %s: %s -> %s (port %s)", dpid, src, dst, in_port)

        # 1. Map the Source MAC to the Port it arrived from
        # TODO: Store the src MAC mapping to the in_port in self.mac_to_port[dpid]
        

        # 2. Decide the Output Port
        out_port = ofproto.OFPP_FLOOD
        # TODO: Check if dst MAC is already inside self.mac_to_port[dpid]
        # If it is, update the out_port variable to that specific port instead of FLOOD!
        

        actions = [parser.OFPActionOutput(out_port)]

        # 3. Inject a FLOW_MOD rule if we confidently know the destination
        if out_port != ofproto.OFPP_FLOOD:
            # Example provided for constructing a Match
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            
            # Example provided for constructing the FlowMod to be pushed into the hardware
            mod = parser.OFPFlowMod(
                datapath=datapath, 
                priority=1, 
                match=match, 
                actions=actions
            )
            # TODO: Send the FlowMod into the switch! (Recall Lab 06: datapath.send_msg)
            

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        # 4. Forward the current packet out immediately
        # TODO: create the 'out' variable using parser.OFPPacketOut (Recall Lab 06)
        out = None
        
        # TODO: send the 'out' message to the switch
