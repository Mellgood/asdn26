#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class TriangleTopo(Topo):
    def build(self):
        # 1. Add switches
        # TODO: Add s1, s2, s3 (Recall Lab 02: self.addSwitch)
        
        # 2. Add hosts
        # TODO: Add h1, h2
        
        # 3. Add links
        # TODO: Connect s1-s2, s1-s3, s2-s3, h1-s2, h2-s3
        pass

if __name__ == '__main__':
    setLogLevel('info')
    topo = TriangleTopo()
    
    # Initialize Mininet WITHOUT a controller
    # Example provided for controller=None:
    net = Mininet(topo=topo, controller=None)
    
    # TODO: Start net, run CLI, and stop the net
    # ...
