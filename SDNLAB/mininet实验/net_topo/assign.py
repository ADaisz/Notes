#!/usr/bin/env python
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Link,TCLink
 
if '__main__' == __name__:
    net = Mininet(link=TCLink)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')
    r3 = net.addHost('r3')
    r4 = net.addHost('r4')

    Link(h1, r1)
    Link(h2, r4)
    Link(r1, r2)
    Link(r1, r3)
    Link(r2, r4)
    Link(r3, r4)

    net.build()
    h1.cmd("ifconfig h1-eth0 0")
    h1.cmd("ip addr add 192.168.1.1/24 brd + dev h1-eth0")
    h1.cmd("ip route add default via 192.168.1.254")

    h2.cmd("ifconfig h2-eth0 0")
    h2.cmd("ip addr add 192.168.2.1/24 brd + dev h2-eth0")
    h2.cmd("ip route add default via 192.168.2.254")

    r1.cmd("ifconfig r1-eth0 0")
    r1.cmd("ifconfig r1-eth1 0")
    r1.cmd("ifconfig r1-eth2 0")
    r1.cmd("ip addr add 192.168.1.254/24 brd + dev r1-eth0")
    r1.cmd("ip addr add 10.0.0.1/24 brd + dev r1-eth1")
    r1.cmd("ip addr add 30.0.0.1/24 brd + dev r1-eth2")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r1.cmd("ip route add 40.0.0.0/24 via 30.0.0.3")
    r1.cmd("ip route add 20.0.0.0/24 via 10.0.0.2")
    r1.cmd("iptables -t nat -A POSTROUTING -o r1-eth2 -s 192.168.1.0/24 -j MASQUERADE")


    r2.cmd("ifconfig r2-eth0 0")
    r2.cmd("ifconfig r2-eth1 0")
    r2.cmd("ip addr add 10.0.0.2/24 brd + dev r2-eth0")
    r2.cmd("ip addr add 20.0.0.2/24 brd + dev r2-eth1")
    r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("ip route add 192.168.1.0/24 via 10.0.0.1")
    r2.cmd("ip route add 192.168.2.0/24 via 20.0.0.4")
    r2.cmd("iptables -t nat -A POSTROUTING -o r2-eth0 -s 20.0.0.0/24 -j MASQUERADE")


    r3.cmd("ifconfig r3-eth0 0")
    r3.cmd("ifconfig r3-eth1 0")
    r3.cmd("ip addr add 30.0.0.3/24 brd + dev r3-eth0")
    r3.cmd("ip addr add 40.0.0.3/24 brd + dev r3-eth1")
    r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("ip route add 192.168.2.0/24 via 40.0.0.4")
    r3.cmd("ip route add 192.168.1.0/24 via 30.0.0.1")
    r3.cmd("iptables -t nat -A POSTROUTING -o r3-eth1 -s 30.0.0.0/24 -j MASQUERADE")


    r4.cmd("ifconfig r4-eth0 0")
    r4.cmd("ifconfig r4-eth1 0")
    r4.cmd("ifconfig r4-eth2 0")
    r4.cmd("ip addr add 192.168.2.254/24 brd + dev r4-eth0")
    r4.cmd("ip addr add 20.0.0.4/24 brd + dev r4-eth1")
    r4.cmd("ip addr add 40.0.0.4/24 brd + dev r4-eth2")
    r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r4.cmd("ip route add 10.0.0.0/24 via 20.0.0.2")
    r4.cmd("ip route add 30.0.0.0/24 via 40.0.0.3")
    r4.cmd("iptables -t nat -A POSTROUTING -o r4-eth0 -s 192.168.2.0/24 -j MASQUERADE")

    CLI(net)
    net.stop()