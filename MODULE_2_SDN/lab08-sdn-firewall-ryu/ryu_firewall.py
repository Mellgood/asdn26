from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

class RyuFirewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RyuFirewall, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        # The malicious IP we want to block absolutely
        self.BLOCKED_IP = "10.0.0.3"

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
        if eth.ethertype == 34525: return # Ignore IPv6

        # Check if it's an IPv4 packet securely
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
            src_ip = ip_pkt.src
            if src_ip == self.BLOCKED_IP:
                self.logger.warning("FIREWALL: Blocking traffic from %s on DPID %s", src_ip, dpid)
                
                # 1. Action: Empty actions mean DROP in OpenFlow
                # Example provided for DROP action:
                actions = []
                
                # 2. Match: Must explicitly specify eth_type=0x0800 for IP matches
                # Example provided for IP matching:
                match = parser.OFPMatch(eth_type=0x0800, ipv4_src=self.BLOCKED_IP)
                
                # 3. FlowMod: Use a high priority (e.g. 100)
                # TODO: Construct a FlowMod using parser.OFPFlowMod (Recall Lab 07)
                # Pass priority=100 so it overrides normal forwarding rules!
                
                
                # TODO: Push the mod to the switch
                
                
                # Drop the current floating packet silently
                return

        # =======================================================
        # Normal L2 Learning Switch logic (Recall Lab 07)
        # =======================================================
        
        # TODO: Store MAC
        # TODO: Decide port (Lookup or FLOOD)
        # TODO: If not flooding, inject permanent Flow_Mod with priority=1 !
        # TODO: Send Packet_out
        
        pass
