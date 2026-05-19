#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        # 1. Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # 2. Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # 3. Add links
        # Connect core to edge switches with bw=10
        self.addLink(s1, s2, bw=10)
        self.addLink(s1, s3, bw=10)
        
        # Connect hosts to edge switches (unconstrained)
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s3)

if __name__ == '__main__':
    # Set the log level to print useful info
    setLogLevel('info')
    
    # Instantiate the topology
    topo = CustomTopo()
    
    # Initialize Mininet with the CustomTopo, OVSBridge and TCLink
    net = Mininet(topo=topo, switch=OVSBridge, controller=None, link=TCLink)
    
    # Start the network
    net.start()
    
    # Start the CLI
    CLI(net)
    
    # Stop the network after CLI exits
    net.stop()
