## docker学习

- Docker概述
- Docker安装
- Docker命令
  - 镜像命令
  - 容器命令
  - 操作命令
  - 。。。
- Docker镜像
- 容器数据卷
- DockerFile
- Docker网络原理
- IDEA整合Docker
- Docker Compose
- Docker Swarm
- CI\CD Jenkins

## Docker 概述



思想来源于集装箱

将项目连同运行需要的环境一起部署

Docker容器技术，是一种轻量的虚拟化技术

```shell
vm:	Linux centos原生镜像	隔离：需要开启多个虚拟机	几个G
docker: 镜像（最核心的环境）	小巧	秒级启动
```

>聊聊docker

Docker基于GO语言开发！开源项目！！！

官网：[Empowering App Development for Developers | Docker](https://www.docker.com/)

文档地址：[Docker Documentation | Docker Documentation](https://docs.docker.com/)

仓库地址：[Docker Hub Container Image Library | App Containerization](https://hub.docker.com/)



#### Docker能干什么

虚拟技术的缺点：

1. 资源占用大
2. 冗余步骤多
3. 启动慢

比较Docker和虚拟机技术的不同：

- 传统虚拟机，虚拟出一条硬件，运行一个完整的操作系统，然后在这个系统上安装和运行软件
- 容器内的应用直接运行在 宿主机，容器是没有自己的内核的，也没有虚拟我们的硬件，所以就轻便了
- 每个容器间是相互隔离的，每个容器内都有一个属于自己的文件系统，互不影响。

>DevOps(开发，运维)

**应用更快速的交付和部署**

传统：一堆帮助文档，安装程序

Docker:打包镜像发布测试，一键运行

**更便捷的升级和扩缩容**

使用Docker之后，我们部署应用就和搭积木一样！

项目打包为一个镜像，扩展 服务器A,服务器B

**更简单的系统运维**

在容器化之后，我们的开发，测试环境都是高度一致的

**更高效的计算资源利用**

Docker 是内核级的虚拟化，可以在一个物理机上运行多个容器实例！服务器的性能可以被压榨到极致



## Docker安装

#### Docker基本组成

<img src="https://gitee.com/hee_seven/pic-go/raw/master/2021/20210728210310.jpg" alt="img" style="zoom: 50%;" />

镜像（image):

docker镜像就好像一个模板，可以通过这个模板来创建容器服务，

tomcat镜像====>run======>tomcat01容器，

通过这个镜像可以创建多个容器（最终服务运行或者项目运行就是在容器中）。

容器(container):

Docker利用容器技术，独立运行一个或者一个组应用，通过镜像来创建的

启动，停止，删除，基础命令！

简易的linux系统

仓库(repository):

仓库就是存放镜像的地方！

Docker Hub(默认为国外的)

阿里云...都有容器服务器(配置镜像加速！)



#### 安装docker

> 环境准备

1.需要Linux基础

2.centos 7

3.xshell 连接远程服务器

4.环境查看

```
#系统内核3.10以上
uname -r
#系统版本
cat /etc/os-release
```



> 安装

帮助文档：

```shell
#1.卸载旧的版本
yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
                  
#2.需要的安装包
yum install -y yum-utils

#3.设置镜像的仓库
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
    
yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

#4.更新yum软件包索引
yum makecache fast

#5.安装docker相关的 docker-ce 社区版   ee企业版
yum install docker-ce docker-ce-cli containerd.io

#6.启动docker
systemctl start docker

#7.docker version
docker version

#8.测试hello world
docker run hello-world
#9. docker images
docker images

#10.卸载依赖 删除资源
yum remove docker-ce docker-ce-cli containerd.io

#docker默认工作路径
rm -rf /var/lib/docker
rm -rf /var/lib/containerd
```

阿里云镜像加速：

 ```
 sudo mkdir -p /etc/docker
 
 sudo tee /etc/docker/daemon.json <<-'EOF'
 {
 	"registry-mirrors":["https://qiyb9988.mirror.aliyuncs.com"]
 }
 EOF
 
 sudo systemctl daemon-reload
 sudo systemctl restart docker
 ```



## 常见命令

#### 1.镜像命令

```shell
#搜索镜像
docker search command

#下载镜像————分层下载
docker pull command

#删除镜像
docker rmi -f 容器id 容器id	#删除部分容器
docker rmi -f $(docker images -aq)#删除全部iamges

```

![image-20210724153028779](E:\image\image-20210724153028779.png)



#### 2.容器命令

说明：我们有镜像才可以创建容器

```
docker pull centos
```

新建容器并启动

```shell
docker run [可选参数] image

#参数说明
--name="name"	容器名字，用来区分容器
-d				后台方式
-it				使用交互方式运行，进入容器查看
-p				指定容器端口 -p 8080:8080

```

```bash
[root@localhost sz]# docker images
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
centos       latest    300e315adb2f   7 months ago   209MB
[root@localhost sz]# docker run -it centos /bin/bash
[root@ae9e3127c818 /]# ls
bin  etc   lib	  lost+found  mnt  proc  run   srv  tmp  var
dev  home  lib64  media       opt  root  sbin  sys  usr
[root@ae9e3127c818 /]#
```

退出容器

```
exit	#退出并停止
ctrl + d    #退出并停止
ctrl + P + Q #退出，容器不停止
```

列出所有运行的容器

```shell
#显示当前运行的容器
docker ps 
docker ps -a 	#显示历史记录
-n	#个数
-q

```

 ```shell
 [root@localhost sz]# docker ps -a
 CONTAINER ID   IMAGE          COMMAND       CREATED             STATUS                         PORTS     NAMES
 ae9e3127c818   centos         "/bin/bash"   5 minutes ago       Exited (0) 3 minutes ago                 strange_bardeen
 c812a0d69afa   d1165f221234   "/hello"      55 minutes ago      Exited (0) 55 minutes ago                determined_lederberg
 b135662664a4   d1165f221234   "/hello"      About an hour ago   Exited (0) About an hour ago             busy_bhabha
 [root@localhost sz]# 
 
 ```

删除容器

```
docker rm id	#正在运行的无法删除
docker rm -f $(docker ps -aq)	#删除所有的容器
```



## 常用其他命令

#### 后台启动容器

```shell
docker run -d centos
#docker 容器使用后台运行，就必须要有前台进程，当没有前台进程时，会自动停止。
```

#### 查看日志

```
docker logs -tf --tail 10 容器id
```

#### 查看容器信息

```
docker inspect 容器id
```

#### 进入当前正在运行的容器

```shell
#方法1		进入容器后开启新终端
docker exec -it 容器id /bin/bash
#方法2		进入正在执行的进程
docker attach 容器id
```

#### 从容器内拷贝文件到主机

```
docker cp 容器id:/home/a.txt /home

#卷可以将容器与主机打通
```

## 练习

#### 1.部署nginx

```shell
docker search nginx --filter=STARS=500
docker pull nginx
docker images
docker run -d --name nginx01 -p 3344:80 nginx
docker ps
curl localhsot:3344
```

2.部署tomcat

```shell
#用完即删除————一般用于测试
docker run -it --rm tomcat:9.0

#正确用法
docker pull tomcat
docker run -d --name tomcat01 -p 3355:8080 tomcat
docker exec  -it tomcat01 /bin/bash
#发现问题 
1.linux 命令少了
2.没有webapps
阿里云镜像的问题，默认最小镜像，所有不必要的都删除，保证最小的命令
```



## Docker图形化界面

#### 1.portainer

```shell
 docker run -d -p 8088:9000	\
 --restart=always -v /var/run/docker.sock:/var/run/docker.sock --privileged=true portainer/portainer
```

![image-20210724175423984](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210728210336.png)

## Docker镜像讲解

镜像是一种轻量级、可执行的独立软件包

>UnionFS(联合系统文件）

是一种分层、轻量级



## Docker容器卷

数据？如果数据在容器中，当容器删除时，数据就会丢失。

$\textcolor{red}{需求：数据可以持久化} $

数据卷的作用：容器之间可以有一个数据共享的技术！Docker容器中产生的数据，同步到本地！

这就是卷技术！目录的挂载，将我们容器内的目录，挂载到linux上面！



总结：容器的持久化和同步操作！容器间也是可以数据共享！



#### 使用卷

> 方式一：直接使用命令来挂载  -v

 ```shell
 docker run -it -v 主机目录：容器内目录
 
 #测试
 docker run -it -v /home/ceshi:/home centos /bin/bash
 #启动起来后我们可以通过 docker inspect 容器id查看
 ```





具名挂载和匿名挂载

```bash
#匿名挂载
-v 容器内路径
docker run -d -P --name nginx01 -v /etc/nginx nginx


docker volume ls


#具名挂载
docker run -d -P --name nginx02 -v juming-nginx:/etc/nginx nginx

#查看挂载的地址
docker volume inspect juming-nginx


```

所有docker容器内的卷，没有指定目录的情况下都是在 `/var/lib/docker/volumes/xxx/_data`

```bash
#如何确定是具名挂载还是匿名挂载
-v 容器内路径		  #匿名挂载
-v 具名：容器内路径		#具名挂载
-v /主机路径：容器内路径#指定路径挂载

```

拓展：

```bash
-v 容器内路径：ro		#改变读写权限

ro:readonly		#只能通过宿主机来操作，容器内是无法操作的！
rw:readwrite

```



## 初识Dockerfile

Dockerfie 就是用来构建docker镜像的构建文件！

```dockerfile
#创建一个dockerfile 建议名字为Dockerfile

FROM centos
VOLUME ["volume1","volume2"]
CMD echo"-----end------"
CMD /bin/bash
```

==执行命令：docker build -f /home/docker/dockerfile1 -t sz/centos:1.0 .==

进入容器后发现：

![image-20210727130546558](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210728210344.png)

查看卷挂载路径：

```bash
docker inspect 容器id
```

![image-20210727130924175](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210728210348.png)



## 数据卷容器

多个容器之间的同步！！！

![image-20210727131240192](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210728210353.png)

```bash
#启动三个容器

```



## DockerFile指令

```
FROM		# 基础镜像
MAINTAINER	# 镜像是谁写的，姓名+邮箱
RUN			# 镜像构建的时候需要运行的命令
ADD			# 添加内容，如压缩包
COPY		# 类似ADD,文件拷贝
WORKDIR		# 镜像工作目录
VOLUME		# 挂载的目录
EXPOSE		# 保留端口配置
CMD			# 指定这个容器启动的时候要运行的命令，只有最后一个会生效，可以被替代
ENTRYPOINT	# 同CMD，不过可以追加
ONBUILD		# 当构建一个被继承 Dockerfile 这个时候就会运行 onbuild 指令，触发指令
ENV			# 构建时设置环境变量
```



#### 实战测试

1. 编写dockerfile文件

   ```
   
   ```

2. 通过这个文件构建镜像

   ```bash
   docker build -f mydockerfile-centos -t mycentos:0.1 .
   ```

![image-20210731195435110](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210731195841.png)

![image-20210731195502208](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210731195858.png)

1. 测试

   ![image-20210731200148664](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210731200149.png)

2. CMD 和 ENTRYPOINT区别

   ```
   cmd 会被追加的命令覆盖
   ```

   

#### 实战：tomcat镜像

1.准备tomcat压缩包，jdk安装包

2.官方默认文件==DockerFile==



#### 发布镜像到dockerhub

1.地址：[Docker Hub](https://hub.docker.com/)，注册自己的账号！！！

2.确定可以登录

3.在自己服务器提交镜像

![image-20210801103418881](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801103420.png)

```shell
docker login -u xiqisz
```

![image-20210801103810655](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801103811.png)

4.提交镜像

![image-20210801104724750](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801104726.png)

```shell
#直接提交会报错
#需要打标签tag

docker tag imageID xiqisz/mycentos:0.1
docker push xiqisz/mycentos:0.1
```

![image-20210801104904694](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801104905.png)

![image-20210801104921303](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801104922.png)



#### 小结

![image-20210801105049190](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801105050.png)



## Docker网络

#### 理解docker0

1.清空所有环境

```bash
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
```

![image-20210801110324258](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801110325.png)

2.测试

```shell
docker run -d -P --name tomcat01 tomcat

#查看容器内部的网络地址	发现容器在启动的时候会得到一个eth0@if9 端口，docker分配的！
docker exec -it tomcat01 ip addr
```

![image-20210801110514821](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801110515.png)

3.ping测试

```shell
#可以ping通
ping 172.17.0.2
```

> 原理

1.我们每启动一个docker容器，docker就会给容器分配一个ip,只要安装了docker，就会有一个docker0桥接模式，使用的技术是veth-pair技术！

再次测试==IP addr==		会多出如此的网卡

![image-20210801111345605](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801111346.png)

```shell
docker和容器之间会生成一对对的网卡
#veth-pair 就是一对的虚拟设备接口，他们成对出现，一段连接着协议，一段彼此相连
```

**容器内部之间可以ping通**

![image-20210801112003899](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801112004.png)

tomcat01和tomcat02是公用的一个路由器，docker0

![image-20210801112510988](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801112512.png)



![image-20210801112911490](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801112912.png)



#### --link

> 思考如下场景:我们编写了一个微服务，database url:ip , 项目不重启，数据库ip换掉了，我们希望可以处理这个问题，可以如何访问容器？

--link 可以直接ping主机

通过在/etc/hosts   中添加其他的主机的ip

#### 自定义网络

==docker0的网络，容器内主机之间不同通过ping主机名ping通==

![image-20210801122201442](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801122202.png)

网络模式：

- bridge	桥接：（默认）
- none     不配置网络
- host      和宿主机共享网络
- container   容器网络联通 （用的少）

测试：

![image-20210801122844567](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801122845.png)

```shell
docker network inspect mynet
```

![image-20210801123543966](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801123545.png)



#### 网络连通

测试如下连接：

![image-20210801123858733](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801123859.png)

![image-20210801124045236](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801124046.png)

```shell
#测试打通tomcat_01 与tomcat01

docker network connect mynet tomcat_01

#连通之后如下所示：
docker network inspect mynet
```

![image-20210801124212172](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801124213.png)

```shell
#一个容器两个ip地址
```



#### 实战：部署radis集群

```shell
#创建网络
docker network create redis --subnet 172.38.0.0/16

#脚本床建redis配置
for port in $(seq 1 6);\
do \
mkdir -p /mydata/redis/node-${port}/conf
touch /mydata/redis/node-${port}/conf/redis.conf
cat << EOF >/mydata/redis/node-${port}/conf/redis.conf
port 6379
bind 0.0.0.0
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-announce-ip 172.38.0.1${port}
cluster-announce-port 6379
cluster-announce-bus-port 6379
appendonly yes
EOF
done

#部署容器
for port in $(seq 1 6);\
do \
docker run -p 637${port}:6379 -p 1637${port}:16379 --name redis-${port} \
-v /mydata/redis/node-${port}/data:/data \
-v /mydata/redis/node-${port}/conf/redis.conf:/etc/redis/redis.conf \
-d --net redis --ip 172.38.0.1${port} redis:5.0.9-alpine3.11 redis-server /etc/redis/redis.conf; \
done

```

![image-20210801130629834](https://gitee.com/hee_seven/pic-go/raw/master/2021/20210801130630.png)



```redis
#运行出错了.redis部分没学过
redis-cli --cluster create  172.38.0.11:6379 172.38.0.12:6379 172.38.0.13.6379 172.38.0.14:6379 172.38.0.15:6379 172.38.0.16.6379 --cluster-replicas 1
```









