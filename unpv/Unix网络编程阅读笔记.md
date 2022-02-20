## Unix网络编程

### 1、概述

#### 1.1时间获取客户程序——适用于`IPV4`的

```c
//该头文件包含大部分网络程序都需要的许多系统头文件，并且定义了诸如MAXLINE的常数
#include	"unp.h"
int main(int argc,char **argv)
{
	int sockkfd,n;
    char revcline[MAXLINE+1];
    struct sockaddr_in servaddr;
    
    if(argc != 2)
        err_quit("usage:a.out <IPaddress>");
    //socket()函数创建了一个网际(AF_INET)字节流(SOCKET_STREAM)套接字
    if((sockfd = socket(AF_INET,SOCK_STREAM,0)) < 0)
        err_sys("socket error");
    
    bzero(&servaddr,sizeof(servaddr));	//清空结构体
    servaddr.sin_family = AF_INET;	//置地址族为AF_INET
    servaddr.sin_port   = htons(13);//时间获取服务器的端口号
    if(inet_pton(AF_INET,argv[1],&servaddr.sin_addr) <= 0)	//转换数据格式
        err_quit("inet_pton error for %s,argv[1]");
    //#define SA	struct sockaddr	通用套接字地址
    if(connect(sockfd,(SA*) &servaddr,sizeof(servaddr)) < 0)
        err_sys("connect error");
    //读取服务器的应答
    while( (n = read(sockfd,recvline,MAXLINE)) > 0){
		recvline[n] = 0;	/*null terminate*/
        if(fputs(recvline,stdout) == EOF)
            err_sys("fputs error");
        
    }
    if(n < 0)
        err_sys("read error");
    exit(0);
}
```

错误处理——采用包裹函数

每个包裹函数完成实际的函数调用，检查返回值，并在发生错误时，终止进程。

```
int Socket(int family ,int type ,int protocol){
	int	n;
	if((n = socket(family,type,protocol)) < 0 )
		err_sys("socket error");
	return n;
}
```



### 1.2TCP时间获取服务器程序

```c
#include	"unp.h"
#include	<ctime.h>
int main(int argc,char **argv)
{	
    int	listenfd,connfd;
    struct sockaddr_in	servaddr;
    char	buff[MAXLINE];
    time_t	ticks;
    //创建TCP套接字
    listenfd = Socket(AF_INET,SOCK_STREAM,0);
    //把服务器的众所周知端口捆绑到套接字
    bzero(&servaddr,sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(13);	/*daytime server*/
    Bind(listenfd,(SA*) &servaddr,sizeof(servaddr));
    
    //把套接字转换成监听套接字
    Listen(listenfd,LISTENQ);
    for(;;){
        //接受客户连接，发送应答
        /*TCP三次握手结束后，accept返回connfd已连接描述符*/
        //accept为每个连接到本服务器的客户返回一个新描述符
		connfd = Accept(listenfd,(SA*)NULL,NULL);
        
        ticks = time(NULL);	//返回国际标准时间的秒数
        //ctime库函数把该整数值转化为时间格式	Mon May 26 20:58:40 2021
        //snprintf要求第二个参数指定目的缓冲区大小，因此可以确保该缓冲区不溢出。
        snprintf(buff,sizeof(buff),"%.24s\r\n",ctime(&ticks));
        Write(connfd,buff,strlen(buff));
        //终止连接
        Close(connfd);
    }
}
```



`size_t`数据类型	————`malloc`唯一参数，`read` `write` 的第三个参数——————64位值

套接字`API`对套接字地址结构的长度使用 `socklen_t`数据类型

`XTI`使用`t_scalar_t`和`t_uscalar_t`数据类型



## 第二章

![image-20210801164315507](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801164317.png)

SCTP提供基于主机的多宿特性，单个SCTP端点可以支持多个IP地址。达到增强应对网络故障的健壮性。           

#### 2.1 `TCP`三路握手、`TCP`的连接终止序列、`TCP`的`TIME_WAIT`状态

##### 2.1.1 三路握手

1. 服务器必须准备好接受外来的连接。

   通常通过调用socket、bind和listen这三个函数来完成，我们称之为被动打开。(passive open)

2. 客户通过调用connect发起主动打开(active open)。

   这时客户`TCP`发送一个`SYN`分节，告诉服务器客户将在待建立的连接中发送的数据的初始序列号。通常`SYN`分节不携带数据，其所在的`IP`数据报只含有一个`IP`首部及可能有的`TCP`选项。

3. 服务器必须确认(`ACK`)客户的SYN，同时自己也得发送一个`SYN`分节，它含有服务器将在同一连接中发送的数据的初始序列号。服务器在单个分节中发送`SYN`和对客户`SYN`的`ACK`。

4. 客户必须确认服务器的`SYN`。

   ![image-20210801173323752](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801173325.png)

这种交换至少需要3个分组，因此称为TCP的三路握手。



#####  2.1.2 TCP连接终止

1. 某个应用进程首先调用close,我们称该端执行主动关闭(active close)。该端的TCP发送一个FIN分节，表示数据发送完毕。
2. 接受到这个`FIN`的对端执行被动关闭(passive close)。这个`FIN`由`TCP`确认。它的接收也作为一个文件结束符(end-of-file)传递给接收端应用进程(放在已排队等候该应用进程接收的任何其他数据之后)，因为`FIN`的接收意味着接收端应用进程在相应连接上再无额外数据接收。
3. 一段时间后，接收到这个文件结束符的应用进程将调用close关闭它的套接字。这导致它的`TCP`也发送一个`FIN`。
4. 接收这个最终`FIN`的原发送端`TCP`(即执行主动关闭的那一端)确认这个`FIN`。

<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801185518.png" alt="image-20210801185516558" style="zoom: 80%;" />

==当一个UNIX进程无论资源的(调用exit or 从main函数返回)还是非自愿的(收到一个终止本进程的信号)终止时，所有打开的描述符都被关闭，这也导致仍然打开的任何TCP连接上也发出一个FIN==



##### 2.1.3 TCP状态转换图

<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801190849.png" alt="image-20210801190848437" style="zoom:80%;" />



<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801191057.png" alt="image-20210801191056115" style="zoom:80%;" />



##### 2.1.4 TIME_WAIT

1. 可靠地实现`TCP`全双工连接的终止

2. 允许老的重复分节在网络中消逝

   防止来自某个连接的老的重复分组在该连接已终止后再现，从而被误解为属于同一连接的某个新的化身。



#### 2.2 `SCTP`的四路握手和`SCTP`的连接终止

##### 2.2.1四路握手

![image-20210801195310530](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801195312.png)

与TCP的差别：

​	作为`SCTP`整体一部分的`cookie`的生成。`INIT`承载一个验证标记`Ta`和一个初始序列号`J`。在关联的有效期内，验证标记`Ta`必须在对端发送的每个分组中出现。初始序列`J`用作承载用户数据的`DATA`块的起始序列号。对端也在`INIT` `ACK`中承载一个验证标记`Tz`，在关联的有效期内，验证标记`Tz`也必须在其发送的每个分组中出现。

除了验证标记`Tz`和初始序列号`K`外，`INIT`的接收端还在作为响应的`INIT ACK`中提供一个`cookieC`。该`cookie`包含设置本`SCTP`关联所需的所有状态，这样服务器的`SCTP`栈就不必保存所关联客户的有关信息。



##### 2.2.2 关联终止

![image-20210801201702774](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801201703.png)

​	`SCTP`没有类似于`TCP`的`TIME_WAIT`状态，因为`SCTP`使用了验证标记。所有后续块都在捆绑它们的`SCTP`分组的公共首部标记了初始的`INIT`块和`INIT ACK`块中作为起始标记交换的验证标记;由来自旧连接的块通过所在`SCTP`分组的公共首部间接携带的验证标记对于新连接来说是不正确的。因此，`SCTP`通过放置验证标记值就避免了`TCP`在`TIME_WAIT`状态保持整个连接的做法。

#### 2.3 套接字层提供的`TCP`、`UDP`、`SCTP`缓冲机制

UDP write调用成功返回表示所写的数据报或其所有片段已加入数据链路层的输出队列

TCP write调用成功返回仅仅表示可以重新使用原来的应用进程缓冲区



## 第三章

#### IPV4 套接字地址结构

```c

//	/usr/include/netinet/in.h

/* Internet address.  */
typedef uint32_t	in_addr_t;
struct in_addr {
	in_addr_t	s_addr;			/* 32-bit IPv4 address */
};

/* Type to represent a port.  */
typedef uint16_t	in_port_t;


struct sockaddr_in {
	uint8_t			sin_len;		/* length of structure (16)*/
	sa_family_t 	sin_family;		/* AF_INET */    
    in_port_t		sin_port;		/* 16-bit TCP or UDP port number */
    struct in_addr	sin_addr;		/* 32-bit IPv4 address */
    char			sin_zero[8];	/* unused */
    
};

```

![image-20210802140546012](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210802140547.png)



#### 通用套接字地址结构

各种套接字地址结构是采用指针传参，向套接字函数传递参数的。

所以，套接字函数需要处理来自所有支持的任何协议族的套接字地址结构。

套接字函数是在ANSI C之前定义的，(当时还没有所谓的void *)，故定义一个通用的套接字地址结构。

这就要求指针传参时需要进行强制类型转换。



作用：对指向特定于协议的套接字地址结构的指针执行强制类型转换。

从内核角度看，内核必须取调用者的指针，把它类型强制转换为 struct sockaddr * 类型，然后检查其中 sa_family 字段的值来确定这个结构的真实类型。

从应用开发人员角度看，void *如果可以使用的化，直接无需强制类型转换。

  



#### 值-结果参数

进程到内核传递套接字地址结构的函数：bind、connect 和sendto 。

```c
struct sockaddr_in serv;

connect(sockfd,(SA *)&serv,sizeof(serv));
```

<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210802155604.png" alt="image-20210802155603189" style="zoom:50%;" />



内核到进程传递套接字地址结构的函数: accept、recvfrom、getsockname、getpeername 。

```c
struct sockaddr_un cli;
socklen_t len;
len = sizeof(cli);

getpeername(unixfd , (SA *) &cli , &len);
```

<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210802155922.png" alt="image-20210802155921628" style="zoom:67%;" />



区别：套接字地址结构大小这一参数，从一个整数改为指向整数变量的指针。

原因：当函数被调用时，结构大小是一个值(value), 他告诉内核在写结构时不至于越界；

​				当函数返回时，结构大小又是一个结果(result),它告诉进程内核在该结构中究竟存了多少信息。





#### 基础函数



































