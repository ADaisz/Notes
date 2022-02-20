
### 0.环境配置

本书源码下载地址 [http://www.unpbook.com](http://www.unpbook.com/)  
解压`tar -zxvf unpv13e.tar.gz`

```shell
cd unpv13e

[root@localhost unpv13e]# ls

[root@localhost unpv13e]# ./configure 
......
configure: creating ./config.status
config.status: creating Makefile
config.status: creating Make.defines
config.status: creating config.h


[root@localhost unpv13e]# cd ./lib
[root@localhost lib]# make
......
ranlib ../libunp.a

[root@localhost lib]# cd ../libfree
[root@localhost libfree]# make
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o in_cksum.o in_cksum.c
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o inet_ntop.o inet_ntop.c
inet_ntop.c: In function ‘inet_ntop’:
inet_ntop.c:60:9: error: argument ‘size’ doesn’t match prototype
  size_t size;
         ^
In file included from inet_ntop.c:27:0:
/usr/include/arpa/inet.h:64:20: error: prototype declaration
 extern const char *inet_ntop (int __af, const void *__restrict __cp,
                    ^
make: *** [inet_ntop.o] Error 1
#报如上错误
#打开当前目录下的inet_ntop.c
#将第60行的 size_t size 修改为 socklen_t size 
#再次make
[root@localhost libfree]# 
[root@localhost libfree]# make
#如下警告不用管
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o inet_ntop.o inet_ntop.c
/usr/include/arpa/inet.h: In function ‘inet_ntop’:
inet_ntop.c:152:23: warning: ‘best.len’ may be used uninitialized in this function [-Wmaybe-uninitialized]
   if (best.base == -1 || cur.len > best.len)
                       ^
inet_ntop.c:123:28: note: ‘best.len’ was declared here
  struct { int base, len; } best, cur;
                            ^
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o inet_pton.o inet_pton.c
ar rv ../libunp.a in_cksum.o inet_ntop.o inet_pton.o
a - in_cksum.o
a - inet_ntop.o
a - inet_pton.o
ranlib ../libunp.a


###### 用root权限将以上编译生成的libunp.a 文件复制到/usr/lib目录中
[root@localhost libfree]# cd ..
[root@localhost unpv13e]# sudo cp libunp.a /usr/lib

##
##测试代码
##
##在另一个终端中打开服务端
[root@localhost unix]# cd unpv13e/
[root@localhost unpv13e]# cd intro
[root@localhost intro]# make daytimetcpsrv
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o daytimetcpsrv.o daytimetcpsrv.c
gcc -I../lib -g -O2 -D_REENTRANT -Wall -o daytimetcpsrv daytimetcpsrv.o ../libunp.a -lpthread
[root@localhost intro]# sudo ./daytimetcpsrv 


#
#客户端
[root@localhost unpv13e]# cd intro
[root@localhost intro]# make daytimetcpcli
gcc -I../lib -g -O2 -D_REENTRANT -Wall   -c -o daytimetcpcli.o daytimetcpcli.c
gcc -I../lib -g -O2 -D_REENTRANT -Wall -o daytimetcpcli daytimetcpcli.o ../libunp.a -lpthread
[root@localhost intro]# sudo ./daytimetcpcli 127.0.0.1
Sun Aug  1 00:11:38 2021
[root@localhost intro]# 

```

