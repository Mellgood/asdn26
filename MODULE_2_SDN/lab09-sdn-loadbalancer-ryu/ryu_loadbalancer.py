from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

class RyuLoadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RyuLoadBalancer, self).__init__(*args, **kwargs)
        self.VIP = "10.0.0.100"
        self.SERVERS = ["10.0.0.2", "10.0.0.3"]
        self.server_turn = 0

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        
        pkt = packet.Packet(msg.data)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        
        if not ip_pkt: 
            return # Only Load balance IPv4 for simplicity
            
        src_ip = ip_pkt.src
        dst_ip = ip_pkt.dst

        # 1. Forwarding towards the VIP
        if dst_ip == self.VIP:
            target_ip = self.SERVERS[self.server_turn]
            self.server_turn = (self.server_turn + 1) % len(self.SERVERS)
            
            self.logger.info("LB: Rewriting VIP req from %s to Server %s", src_ip, target_ip)
            
            # Example provided for SET_FIELD, which modifies the packet header natively!
            actions = [
                parser.OFPActionSetField(ipv4_dst=target_ip),
                # We'd typically output to the correct port, we just flood here for brevity
                parser.OFPActionOutput(ofproto.OFPP_FLOOD) 
            ]
            
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                      in_port=in_port, actions=actions, data=msg.data)
            datapath.send_msg(out)
            return
            
        # 2. Returning from the Servers to the Client
        if src_ip in self.SERVERS:
            # We must disguise the reply as coming back from the VIP
            # TODO: Add a parser.OFPActionSetField to rewrite ipv4_src to self.VIP
            actions = [
                # ...
            ]
            
            # TODO: Add the output action and send the PacketOut
            # ...
            return
