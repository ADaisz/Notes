!usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

class Mytopo( Topo ):
    "simple topology example."
    def __init__(self):
        "Create custom topo."
        #Initialize topology
        Topo.__init__(self)
        #Add hosts and Switches
        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')
        Switch1 = self.addSwitch('s1')
        Switch2 = self.addSwitch('s2')

        #Add links
        self.addLink(Host1,Switch1)
        self.addLink(Host2,Switch1)
        self.addLink(Host3,Switch2)
        self.addLink(Switch1,Switch2)
topos = { 'mytopo': ( lambda: Mytopo() ) }


        

