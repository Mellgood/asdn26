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
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # 2. Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # 3. Add links
        # Links between switches with 10 Mbps bandwidth constraint
        self.addLink(s1, s2, bw=10)
        self.addLink(s1, s3, bw=10)
        
        # Unconstrained links for hosts
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s3)

if __name__ == '__main__':
    # Set the log level to print useful info
    setLogLevel('info')
    
    # Instantiate the topology
    topo = CustomTopo()
    
    # Initialize Mininet with the CustomTopo, OVSController and TCLink
    # TCLink is mandatory to enforce the bandwidth constraints (bw)
    net = Mininet(topo=topo, controller=OVSController, link=TCLink)
    
    # Start the network
    net.start()
    
    # Open the Mininet CLI
    CLI(net)
    
    # Stop the network cleanly when the CLI is closed
    net.stop()
