#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class TriangleTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Add links
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s3)
        
        self.addLink(h1, s2)
        self.addLink(h2, s3)

if __name__ == '__main__':
    setLogLevel('info')
    topo = TriangleTopo()
    
    # Initialize Mininet WITHOUT a controller
    net = Mininet(topo=topo, controller=None)
    
    # Start net, run CLI, and stop the net
    net.start()
    CLI(net)
    net.stop()
