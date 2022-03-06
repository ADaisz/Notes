### reference
http://csie.nqu.edu.tw/smallko/sdn/sdn.htm

### mininet 测试
1.  loss

```
##以tcp连接，5%的丢包率运行
mn --link=tc,loss=5

mininet>h1 ping -c 1000 -i 0.01 h2

##结果显示丢包率大约为18%
##原因：1-(1-5%)^4 =18...%
```


2.  iperf

```
mn --link=tc,loss=0,bw=10

mininet>xterm h1 h2

### h1作为client 以udp形式，设置带宽为20M,传输10次
h1# iperf -c 10.0.0.2 -u -b 20M -t 10

### h2 作为server 以1s间隔输出结果,以udp形式
h2# iperf -s -i 1 -u

##结果显示Bandwidth为9.7Mbits/sec
```

3.  delay

```
mn --link=tc,loss=0,bw=10,delay='10ms'

mininet> h1 ping -c 10 h2

##结果:time结果为41.5ms(来回四次+交换机处理时延)

```


### iperf 绘图

下载绘图工具
```
apt install gnuplot
```
```
xterm h1 h2

h1#iperf -c 10.0.0.2 -t 10

h2#iperf -s -i 1 | tee tcp.txt

```

![](./iperf_plot/iperf.png)

```
## 选取前十行
cat tcp.txt | grep sec |head -n 10 | tr "-" " " | awk '{print $4,$8}' > a


###显示结果
1.0 9.07
2.0 9.56
3.0 9.55
4.0 9.57
5.0 9.56
6.0 9.57
7.0 9.57
8.0 9.58
9.0 9.55
10.0 9.56
```

绘图
```
ubuntu$ gnuplot

gunplot>plot "a" title "tcp" with linespoints
gnuplot>set yrange[0:10];set ytics 0,1,10;set xrange[0:10];set xtics 0,1,10;replot
gnuplot>set xlabel "time(sec)";set ylabel "throughput(Mbps)";set title "TCP Throughput";replot
gnuplot>set terminal gif;set output "a.gif"
gnuplot>replot
```
结果
![](./iperf_plot/a.gif)

### mininet Script

前三个简单的直接跳过

1.  编写4.py脚本构造如下的拓扑

![4](./net_topo/4.png)

[代码见4.py](./net_topo/4.py)


1.  编写5.py脚本构造如下的拓扑

![5](./net_topo/5.png)

[代码见5.py](./net_topo/5.py)


3.  作业：构造如下的拓扑

![assign](./net_topo/assign.png)

Tips:
```
##复制时出现空白行
sed -i '/^$/d ' 2.py
```

```
##清除ip
ifconfig h1-eth0 0

##设置ip
ifconfig h1-eth0 192.168.1.1/24
ip route add default via 192.168.1.254

```



### Bridge

安装bridge相关包
```
sudo apt install bridge-utils
```

1. [br1.py](./bridge/br1.py)


![](./bridge/br1.png)


2.  [br2.py](./bridge/br2.py)


![](./bridge/br2.png)


3.  [br3.py](./bridge/br3.py)

![](./bridge/br3.png)


### VLAN + bridge

安装vlan
```
sudo apt install vlan
```
4.  [br4.py](./vlan/br4.py)

![](./vlan/br4.png)

### OVS

1.  controller 消失

```
sudo mn --topo single,2

mininet>h1 ping h2 

##成功

##当把controller进程杀死时，ping 失败
```
![kill](./OVS/kill_controller.png)
杀死进程后
![ping_fail](./OVS/ping_fail.png)

2.  解决办法

