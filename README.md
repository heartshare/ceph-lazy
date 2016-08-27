# ceph-lazy - Complex Ceph query tool


Ceph-lazy - Be efficient, be lazy !


## 本项目重构自哪里

项目的是基于 https://github.com/gcharot/ceph-lazy这个项目做的python版本的

## 关于我

略懂ceph，但是对python几乎空白，用比较原始的方式，基本实现了需要的功能，修改了原作者在两个地方的小bug，欢迎试用并且提出自己的需求，我可以根据需要进行一些新的功能的加入

## 这是什么

Ceph的CLI是非常完整的，它可以几乎做一切查询。但有时候需要做一些复杂的过滤，你经常忘记把它们记下来，在下一次使用的时候又需要重来一遍

例如 获得真正的RBD图像尺寸，从一个特定的OSD列出所有主要PG或更复杂的像得到RBD image的所在的OSD​​或存储主机查询。

Ceph-lazy就是为你准备的，让你不需要再去使用管道命令，并且很快得到你想要的结果。

Ceph-lazy不会在您的集群上执行任何写操作，只会读取，所以放心的使用


## 我能做什么

Ceph-lazy 当前被分成了五类操作 Host - PGs - RBD - OSD and Objects; 每个类型的提供了几个命令.需求查看支持哪些命令，可以使用命令加上参数 `-h` 或者不加参数，直接敲ceph-lazy命令 
分类是根据输入的数据的，host查询的就是host相关的，rbd就是查询rbd相关的，很明显！

当前支持的操作如下 : 

    Host
    -----
    host-get-osd      hostname                      列出节点上的所有的OSD.
    host-get-nodes                                  列出所有的存储节点.
    host-osd-usage    hostname        [detail]      列出存储节点上的存储使用的情况(detail看详细信息).
    host-all-usage                    [detail]      列出所有存储节点上的存储使用的情况(detail看详细信息)


    Placement groups
    -----------------
    pg-get-host       pgid                          列出PG所在的节点(first is primary) 
    pg-most-write                                   列出写操作最多的PG ( operations number)
    pg-less-write                                   列出写操作最少的PG ( operations number)
    pg-most-write-kb                                列出写操作最多的PG (data written)
    pg-less-write-kb                                列出写操作最少的PG (data written)
    pg-most-read                                    列出读操作最多的PG (operations number)
    pg-less-read                                    列出读操作最少的PG (operations number)
    pg-most-read-kb                                 列出读操作最多的PG (data read)
    pg-less-read-kb                                 列出读操作最少的PG (data read)
    pg-empty                                        列出空的PG (没有存储对象)

    RBD
    ----
    rbd-prefix        pool_name image_name          列出RBD的prefix
    rbd-count         pool_name image_name          列出RBD的对象数目
    rbd-host          pool_name image_name          列出RBD的Primary所在的存储主机
    rbd-osd           pool_name image_name          列出RBD的Primary所在的OSD节点
    rbd-size          pool_name image_name          列出RBD的Image的真实大小
    rbd-all-size      pool_name                     列出指定存储所有的RBD的Image的真实大小(Top first)

    OSD
    ----
    osd-most-used                                   列出容量使用最多的OSD
    osd-less-used                                   列出容量使用最少的OSD
    osd-get-ppg       osd_id                        列出指定OSD上所有的primary PG
    osd-get-pg        osd_id                        列出指定OSD上的所有PG

    Objects
    --------
    object-get-host   pool_name object_id           列出指定对象所在的主机（第一个是主）


## 依赖什么

你的服务器上需要有这几个命令(ceph, rados, rbd, osdmaptool)，原作者因为是shell下面使用了jq解析json，而python可以直接解析json。所以没有依赖

你运行命令的机器上需要有查询的权限，当然最简单的办法就是关闭掉ceph 的auth


## 安装方法

Usage is pretty straightforward just ensure you have all dependencies installed, clone the git repo

```
wget -o /sbin/ceph-lazy https://raw.githubusercontent.com/zphj1987/ceph-lazy/lazy-python/ceph-lazy.py
chmod 777 /sbin/ceph-lazy
```


## 怎么使用

直接运行命令即可:

```
Usage : ceph-lazy  [command] [parameters]
```

## TODO

- 增加更多的错误控制
- 发掘更多的想法
- 改善性能
- 命令补全


##重构进度（完成）

-     host-get-osd      (done)
-     host-get-nodes    (done)                             
-     host-osd-usage    (done)
-     host-all-usage    (done)                             
-     pg-get-host       (done)
-     pg-most-write     (done)                             
-     pg-less-write     (done)                           
-     pg-most-write-kb  (done)                         
-     pg-less-write-kb  (done)                          
-     pg-most-read      (done)                            
-     pg-less-read      (done)                          
-     pg-most-read-kb   (done)                          
-     pg-less-read-kb   (done)                        
-     pg-empty          (done)                            
-     rbd-prefix        (done)
-     rbd-count         (done)
-     rbd-host          (done)
-     rbd-osd           (done) 
-     rbd-size          (done)
-     rbd-all-size      (done)
-     osd-most-used     (done)                             
-     osd-less-used  	(done)                                 
-     osd-get-ppg       (done) 
-     osd-get-pg        (done)
-     object-get-host   (done)
