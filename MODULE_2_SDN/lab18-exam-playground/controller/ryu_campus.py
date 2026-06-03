"""
Ryu Campus Controller — Learning Switch for the Exam Playground

This is a production-ready L2 Learning Switch that manages multiple OVS switches.
It is based on the controller from Lab 07, enhanced with clearer logging.

How it works:
  1. On PACKET_IN, it learns the source MAC → port mapping for each switch (dpid)
  2. If the destination MAC is known, it unicasts to the correct port AND installs
     a flow rule on the switch to handle future packets in hardware
  3. If the destination MAC is unknown, it floods to all ports

You may need to modify this controller during the exam.
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet


class RyuCampusController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    SWITCH_NAMES = {}  # Will be populated as switches connect

    def __init__(self, *args, **kwargs):
        super(RyuCampusController, self).__init__(*args, **kwargs)
        # mac_to_port[dpid][mac_address] = port_number
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Called when a new switch connects. Installs a default table-miss rule."""
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry: send unmatched packets to the controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=0,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

        self.logger.info(">>> Switch connected: dpid=%s", datapath.id)

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

        # Skip IPv6 multicast noise
        if eth.ethertype == 0x86DD:
            return

        self.logger.info("[dpid=%s] PACKET_IN: %s -> %s (in_port=%s)",
                         dpid, src, dst, in_port)

        # 1. Learn: map source MAC to the port it arrived from
        self.mac_to_port[dpid][src] = in_port

        # 2. Decide: unicast if we know the destination, otherwise flood
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # 3. Optimize: install a hardware flow rule for known destinations
        if out_port != ofproto.OFPP_FLOOD:
            self.logger.info("[dpid=%s] FLOW_MOD: %s -> port %s", dpid, dst, out_port)
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=1,
                match=match,
                instructions=inst
            )
            datapath.send_msg(mod)

        # 4. Forward the current packet
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)
