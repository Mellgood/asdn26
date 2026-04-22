from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

class RyuHub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RyuHub, self).__init__(*args, **kwargs)

    # This decorator binds the PACKET_IN event to our handler
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # 1. Action: We want to flood the packet out of all ports.
        # Example provided for constructing an Action in Ryu:
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        
        # Maintain the payload data
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
            
        # 2. Instruction: Construct the PACKET_OUT message using the parser.
        # TODO: create the 'out' variable using parser.OFPPacketOut()
        # hint: pass (datapath=datapath, buffer_id=msg.buffer_id, 
        #             in_port=msg.match['in_port'], actions=actions, data=data)
        out = None
        
        # 3. Execution: Send the message back to the switch to be executed.
        # Example provided for transmitting messages to the datapath:
        # datapath.send_msg(out)
        # TODO: uncomment the line above once 'out' is defined!
