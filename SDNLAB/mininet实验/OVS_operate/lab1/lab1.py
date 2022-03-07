#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink,Intf
from mininet.node import Controller,RemoteController
 
if '__main__' == __name__:
    net = Mininet(link=TCLink)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    c0 = net.addController('c0', controller=RemoteController)
    net.addLink(h1, s1)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s3, s2)
    net.addLink(s2, h2)
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    # rules for s1
    # ovs-ofctl add-flow s1 arp,arp_op=1,arp_spa=10.0.0.1,arp_tpa=10.0.0.2,actions=output:2
    # ovs-ofctl add-flow s1 arp,arp_op=1,arp_spa=10.0.0.2,arp_tpa=10.0.0.1,actions=output:1
    # ovs-ofctl add-flow s1 arp,arp_op=2,arp_spa=10.0.0.1,arp_tpa=10.0.0.2,actions=output:2
    # ovs-ofctl add-flow s1 arp,arp_op=2,arp_spa=10.0.0.2,arp_tpa=10.0.0.1,actions=output:1
    # ovs-ofctl add-flow s1 icmp,nw_src=10.0.0.1,nw_dst=10.0.0.2,icmp_type=8,icmp_code=0,actions=output:2
    # ovs-ofctl add-flow s1 icmp,nw_src=10.0.0.2,nw_dst=10.0.0.1,icmp_type=0,icmp_code=0,actions=output:1

    # rules for s2
    # ovs-ofctl add-flow s2 arp,arp_op=1,arp_spa=10.0.0.1,arp_tpa=10.0.0.2,actions=output:3
    # ovs-ofctl add-flow s2 arp,arp_op=1,arp_spa=10.0.0.2,arp_tpa=10.0.0.1,actions=output:1
    # ovs-ofctl add-flow s2 arp,arp_op=2,arp_spa=10.0.0.1,arp_tpa=10.0.0.2,actions=output:3
    # ovs-ofctl add-flow s2 arp,arp_op=2,arp_spa=10.0.0.2,arp_tpa=10.0.0.1,actions=output:1
    # ovs-ofctl add-flow s2 icmp,nw_src=10.0.0.1,nw_dst=10.0.0.2,icmp_type=8,icmp_code=0,actions=output:3
    # ovs-ofctl add-flow s2 icmp,nw_src=10.0.0.2,nw_dst=10.0.0.1,icmp_type=0,icmp_code=0,actions=output:2

    # rules for s3
    # ovs-ofctl add-flow s3 icmp,nw_src=10.0.0.2,nw_dst=10.0.0.1,icmp_type=0,icmp_code=0,actions=output:1

    CLI(net)
    net.stop()