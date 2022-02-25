#   mininet介绍  
## 一、Mininet是什么

Mininet是由斯坦福大学基于Linux Container架构开发的一个进程虚拟化网络仿真工具，可以创建一个包含主机，交换机，控制器和链路的虚拟网络，其交换机支持OpenFlow，具备高度灵活的自定义软件定义网络。
## 二、Mininet可以做什么

1.  为OpenFlow应用程序提供一个简单，便宜的网络测试平台；  
2.  启用复杂的拓扑测试，无需连接物理网络；
3.  具备拓扑感知和OpenFlow感知的CLI，用于调试或运行网络范围的测试；
4.  支持任意自定义拓扑，主机数可达4096，并包括一组基本的参数化拓扑；
5.  提供用户网络创建和实验的可拓展Python API。

##  三、Mininet的优势

>Mininet结合了许多仿真器，硬件测试床和模拟器的有优点：

1.  与仿真器比较：启动速度快；拓展性大；带宽提供多；方便安装，易使用。
2.  与模拟器比较：可运行真实的代码；容易连接真实的网络。
3.  与硬件测试床比较：便宜；快速重新配置及重新启动。

##  四、Mininet的主要特性

>Mininet作为一个轻量级软定义网络研发和测试平台，其主要特性包括：

1.  支持OpenFlow、Open vSwitch等软定义网络部件；
2.  方便多人协同开发；
3.  支持系统级的还原测试；
4.  支持复杂拓扑、自定义拓扑；
5.  提供python API；
6.  很好的硬件移植性（Linux兼容），结果有更好的说服力；
7.  高扩展性，支持超过4096台主机的网络结构。

#   Mininet安装

>Mininet安装主要有三种方法，安装过程参见(http://mininet.org/download/):
+   使用装有Mininet的虚拟机
+   github获取安装Mininet源代码(推荐)
+   Mininet文件包安装

>方法二简要安装过程：
```
#1. 下载源码
git clone git://github.com/mininet/mininet

#2. 进入mininet/util目录,查看安装选项
./install.sh -h

#3. 安装mininet
./install -n3V 2.5.0  #安装ovs2.5
./install -a          #全部安装
```

# Mininet命令

测试安装是否完成
```
sudo mn --test pingall      #显示Cleanup complete.
```
启动mininet
```
mn
```
常用交互命令
```
#nodes              查看全部节点 
#net                查看链路信息 
#dump               输出各节点的信息 
#h1 ping -c 4 h2    测试主机之间的连通性 
#iperf              两个节点之间用指定简单的 TCP 测试 
#iperfudp           两个节点之间用指定款单 udp 进行测试 
#noecho             运行交互窗口，关闭回应 
#pingpair           两个主机将互 ping 
#help               列出命令文档，查看命令帮助： help command 
#dpctl              流表类操作 
#exit/quit          退出 mininet 命令行 
#hX ifconfig        查看当前那主机的 ip 地址，如： h1 ifconfig 
#py/sh              执行 python 表达式或运行外部 shell 程序 
```
python添加节点
```
py net.addHost('h3')
py net.addLink(s1,net.get('h3'))
py s1.attach('s1-eth3')
py net.get('h3').cmd('ifconfig h3-eth0 10.0.0.3')
```