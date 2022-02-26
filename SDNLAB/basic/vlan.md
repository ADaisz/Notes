## reference
https://info.support.huawei.com/info-finder/encyclopedia/zh/VLAN.html

##  什么是VLAN
VLAN(Virtual Local Area Network),即虚拟局域网。  
>是一个将物理的LAN在逻辑上划分为多个广播域的通信技术。  

每一个VLAN是一个广播域，VLAN内的主机之间可以直接通信，而VLAN间则不能直接互通。这样，广播报文就被限制在一个VLAN内。  

##  为什么需要VLAN

早期以太网是一种基于CSMA/CD（Carrier Sense Multiple Access/Collision Detection）的共享通讯介质的数据网络通讯技术。当主机数目较多时会导致冲突严重、广播泛滥、性能显著下降甚至造成网络不可用等问题。通过二层设备实现LAN互连虽然可以解决冲突严重的问题，但仍然不能隔离广播报文和提升网络质量。  
在这种情况下出现了VLAN技术。这种技术可以把一个LAN划分成多个逻辑的VLAN，每个VLAN是一个广播域，VLAN内的主机间通信就和在一个LAN内一样，而VLAN间则不能直接互通，广播报文就被限制在一个VLAN内。如下图所示。  
![](https://download.huawei.com/mdl/image/download?uuid=31e82e94f6c34998b68ca5c54def78dd)  


**因此，VLAN具备以下优点：**
+   限制广播域：广播域被限制在一个VLAN内，节省了带宽，提高了网络处理能力。
+   增强局域网的安全性：不同VLAN内的报文在传输时相互隔离，即一个VLAN内的用户不能和其它VLAN内的用户直接通信。
+   提高了网络的健壮性：故障被限制在一个VLAN内，本VLAN内的故障不会影响其他VLAN的正常工作。
+   灵活构建虚拟工作组：用VLAN可以划分不同的用户到不同的工作组，同一工作组的用户也不必局限于某一固定的物理范围，网络构建和维护更方便灵活。  

## VLAN VS 子网

通过将IP地址的网络部分进一步划分为若干个子网，可以解决IP地址空间利用率低和两级IP地址不够灵活的问题。

与VLAN相类似的是，子网也可以隔离主机间的通信。属于不同VLAN的主机之间不能直接通信，属于不同的子网的主机之间也不能直接通信。但二者没有必然的对应关系。 

![](https://download.huawei.com/mdl/image/download?uuid=147da9864db1436982755b69d9355464)  


##  VLAN Tag和VLAN ID

要使交换机能够分辨不同VLAN的报文，需要在报文中添加标识VLAN信息的字段。IEEE 802.1Q协议规定，在以太网数据帧中加入4个字节的VLAN标签（又称VLAN Tag，简称Tag），用以标识VLAN信息。  

![](https://download.huawei.com/mdl/image/download?uuid=6b7f04dbe20643d3a42fe55ad4eb6cef)  

数据帧中的VID字段标识了该数据帧所属的VLAN，数据帧只能在其所属VLAN内进行传输。VID字段代表VLAN ID，VLAN ID取值范围是0～4095。由于0和4095为协议保留取值，所以VLAN ID的有效取值范围是1～4094。

交换机内部处理的数据帧都带有VLAN标签。而交换机连接的部分设备（如用户主机、服务器）只会收发不带VLAN tag的传统以太网数据帧。因此，要与这些设备交互，就需要交换机的接口能够识别传统以太网数据帧，并在收发时给帧添加、剥除VLAN标签。添加什么VLAN标签，由接口上的缺省VLAN（Port Default VLAN ID，PVID）决定。

##  VLAN的接口类型和VLAN标签的处理机制
现网中属于同一个VLAN的用户可能会被连接在不同的交换机上，且跨越交换机的VLAN可能不止一个，如果需要用户间的互通，就需要交换机间的接口能够同时识别和发送多个VLAN的数据帧。根据接口连接对象以及对收发数据帧处理的不同，当前有VLAN的多种接口类型，以适应不同的连接和组网。

不同厂商对VLAN接口类型的定义可能不同。对于华为设备来说，常见的VLAN接口类型有三种，包括：Access、Trunk和Hybrid。  
<br/>
![](https://forum.huawei.com/enterprise/zh/data/attachment/forum/dm/ecommunity/uploads/2014/0605/17/539033ee39105.png)  <br/><br/>
### **Access接口**
Access接口一般用于和不能识别Tag的用户终端（如用户主机、服务器）相连，或者不需要区分不同VLAN成员时使用。

在一个VLAN交换网络中，以太网数据帧主要有以下两种形式：  
+   无标记帧（Untagged帧）：原始的、未加入4字节VLAN标签的帧。
+   有标记帧（Tagged帧）：加入了4字节VLAN标签的帧。  

Access接口大部分情况只能收发Untagged帧，且只能为Untagged帧添加唯一VLAN的Tag。交换机内部只处理Tagged帧，所以Access接口需要给收到的数据帧添加VLAN Tag，也就必须配置缺省VLAN。配置缺省VLAN后，该Access接口也就加入了该VLAN。

当Access接口收到带有Tag的帧，并且帧中VID与PVID相同时，Access接口也能接收并处理该帧。

在发送带有Tag的帧前，Access接口会剥离Tag。

### **Trunk接口**
Trunk接口一般用于连接交换机、路由器、AP以及可同时收发Tagged帧和Untagged帧的语音终端。它可以允许多个VLAN的帧带Tag通过，但只允许属于缺省VLAN的帧从该类接口上发出时不带Tag（即剥除Tag）。

Trunk接口上的缺省VLAN，有的厂商也将它定义为native VLAN。当Trunk接口收到Untagged帧时，会为Untagged帧打上Native VLAN对应的Tag。

### **Hybrid接口**
Hybrid接口既可以用于连接不能识别Tag的用户终端（如用户主机、服务器）和网络设备（如Hub），也可以用于连接交换机、路由器以及可同时收发Tagged帧和Untagged帧的语音终端、AP。它可以允许多个VLAN的帧带Tag通过，且允许从该类接口发出的帧根据需要配置某些VLAN的帧带Tag（即不剥除Tag）、某些VLAN的帧不带Tag（即剥除Tag）。

Hybrid接口和Trunk接口在很多应用场景下可以通用，但在某些应用场景下，必须使用Hybrid接口。比如在灵活QinQ中，服务提供商网络的多个VLAN的报文在进入用户网络前，需要剥离外层VLAN Tag，此时Trunk接口不能实现该功能，因为Trunk接口只能使该接口缺省VLAN的报文不带VLAN Tag通过。  

##  VLAN的使用场景  

>VLAN的常见使用场景包括：VLAN间用户的二层隔离，VLAN间用户的三层互访。

### **VLAN间用户的二层隔离**
如下图所示，某商务楼内有多家公司，为了降低成本，多家公司共用网络资源，各公司分别连接到一台二层交换机的不同接口，并通过统一的出口访问Internet。  
![](https://download.huawei.com/mdl/image/download?uuid=b07e3ea07ec04d3c806483ca06846958)  


为了保证各公司业务的独立和安全，可将每个公司所连接的接口划分到不同的VLAN，实现公司间业务数据的完全隔离。可以认为每个公司拥有独立的“虚拟路由器”，每个VLAN就是一个“虚拟工作组”。

再比如，某公司有两个部门，分别分配了固定的IP网段。为加强员工间的学习与交流，员工的位置有时会相互调动，但公司希望各部门员工访问的网络资源的权限不变。  

![](https://download.huawei.com/mdl/image/download?uuid=aac85511d6a440928478e7307d8614cd)  

为了保证部门内员工的位置调整后，访问网络资源的权限不变，可在公司的交换机Switch_1上配置基于IP子网划分VLAN。这样，服务器的不同网段就划分到不同的VLAN，访问服务器不同应用服务的数据流就会隔离，提高了安全性。

### **VLAN间用户的三层互访**
如下图所示，某小型公司的两个部门分别通过二层交换机接入到一台三层交换机Switch_3，所属VLAN分别为VLAN2和VLAN3，部门1和部门2的用户互通时，需要经过三层交换机。  

![](https://download.huawei.com/mdl/image/download?uuid=35ceb2d067304310b72c1cdf5f445b82)  

可在Switch_1和Switch_2上划分VLAN并将VLAN透传到Switch_3上，然后在Switch_3上为每个VLAN配置一个VLANIF接口，实现VLAN2和VLAN3间的路由。

##  云化场景下，VLAN存在的问题
随着网络技术的发展，云计算凭借其在系统利用率高、人力和管理成本低、灵活性和可扩展性强等方面表现出的优势，已经成为目前企业IT建设的新趋势。而服务器虚拟化作为云计算的核心技术之一，得到了越来越多的应用。

VLAN作为传统的网络隔离技术，在标准定义中VLAN的数量只有4096个，无法满足大型数据中心的租户间隔离需求。另外，VLAN的二层范围一般较小且固定，无法支持虚拟机大范围的动态迁移。

因此，RFC定义了VLAN扩展方案VXLAN（Virtual eXtensible Local Area Network，虚拟扩展局域网）。VXLAN采用MAC in UDP（User Datagram Protocol）封装方式，是NVO3（Network Virtualization over Layer 3）中的一种网络虚拟化技术。VXLAN完美地弥补了VLAN的上述不足，一方面通过VXLAN中的24比特VNI（VXLAN Network Identifier）字段，提供多达16M租户的标识能力，远大于VLAN的数量；另一方面，VXLAN本质上在两台交换机之间构建了一条穿越数据中心基础IP网络的虚拟隧道，将数据中心网络虚拟成一个巨型“二层交换机”，满足虚拟机大范围动态迁移的需求。  

具体的VXLAN相关内容，参见[VXLAN](./vxlan.md)