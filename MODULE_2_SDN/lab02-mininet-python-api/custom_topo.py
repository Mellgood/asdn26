#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        # 1. Add switches
        # Example provided for s1:
        s1 = self.addSwitch('s1')
        # TODO: Add s2, s3
        

        # 2. Add hosts
        # Example provided for h1:
        h1 = self.addHost('h1')
        # TODO: Add h2, h3, h4
        

        # 3. Add links
        # Example provided for s1 to s2 with 10 Mbps bandwidth limitation:
        self.addLink(s1, s2, bw=10)
        # TODO: Connect s3 to s1 (with bw=10)
        # TODO: Connect h1, h2 to s2
        # TODO: Connect h3, h4 to s3
        pass

if __name__ == '__main__':
    # Set the log level to print useful info
    setLogLevel('info')
    
    # Instantiate the topology
    topo = CustomTopo()
    
    # TODO: Initialize Mininet with the CustomTopo, OVSController and TCLink
    # Example provided:
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    
    # TODO: Start the network
    # Example provided:
    net.start()
    
    # TODO: Start the CLI
    # ...
    
    # TODO: Stop the network after CLI exits
    # ...
