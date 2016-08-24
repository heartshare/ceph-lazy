# ceph-lazy - Complex Ceph query tool


Ceph-lazy - Be efficient, be lazy !


##重构进度

-     host-get-osd      (done)
-     host-get-nodes    (done)                             
-     host-osd-usage    (done)
-     host-all-usage    (done)                             
-     pg-get-host       (done)
-     pg-most-write                                   
-     pg-less-write                                  
-     pg-most-write-kb                               
-     pg-less-write-kb                                
-     pg-most-read                                    
-     pg-less-read                                   
-     pg-most-read-kb                                 
-     pg-less-read-kb                               
-     pg-empty                                        
-     rbd-prefix       
-     rbd-count         
-     rbd-host         
-     rbd-osd           
-     rbd-size         
-     rbd-all-size      
-     osd-most-used                                   
-     osd-less-used                                   
-     osd-get-ppg      
-     osd-get-pg       
-     object-get-host   



## WHAT IS THAT

Ceph CLI is very complete, it can do pretty much everything. However there are certain tasks that require two or more steps with nasty grep/sed which take time and you usually forget to write them down for the next time.

For example, get the RBD real image size, list all primary PG from a particular OSD or even more complex queries like get all OSDs or nodes that hosts a particular RBD image.
Ceph-lazy does that for you so you don't loose time on piped commands and quickly get the result that you want.

Ceph-lazy DOES NOT perform any write operation on your cluster, ONLY READS.



Ceph的CLI是非常完整的，它可以做几乎一切。但也有需要做一些复杂的过滤，你经常忘记把它们写下来，在下一次使用的时候又需要重来一遍

例如，获得真正的RBD图像尺寸，从一个特定的OSD列出所有主要PG或更复杂的像得到了承载特定RBD图像的所有的OSD​​或节点查询。

Ceph-lazy，对你，让你不要松时间对管道命令，并很快得到你想要的结果。

Ceph的懒不会在您的集群上执行任何写操作，只会读取，所以放心的使用


## WHAT CAN I DO

Ceph-lazy is currently splitted into five categories: Host - PGs - RBD - OSD and Objects; each category offers a number of commands. List of commands can be reviewed by using the -h option or invoking ceph-lazy without any argument. 
Categories mainly refers to the type of input, for example host category will get info at a host level whereas RBD will report RBD information; pretty obvious !

The current set of commands is as follow : 

    Host
    -----
    host-get-osd      hostname                      列出节点上的所有的OSD.
    host-get-nodes                                  列出所有的存储节点.
    host-osd-usage    hostname        [detail]      列出存储节点上的存储使用的情况(detail看详细信息).
    host-all-usage                                  Show total OSD space usage of each nodes (-d for details)


    Placement groups
    -----------------
    pg-get-host       pgid                          Find PG storage hosts (first is primary) 
    pg-most-write                                   Find most written PG (nb operations)
    pg-less-write                                   Find less written PG (nb operations)
    pg-most-write-kb                                Find most written PG (data written)
    pg-less-write-kb                                Find less written PG (data written)
    pg-most-read                                    Find most read PG (nb operations)
    pg-less-read                                    Find less read PG (nb operations)
    pg-most-read-kb                                 Find most read PG (data read)
    pg-less-read-kb                                 Find less read PG (data read)
    pg-empty                                        Find empty PGs (no stored object)

    RBD
    ----
    rbd-prefix        pool_name image_name          Return RBD image prefix
    rbd-count         pool_name image_name          Count number of objects in a RBD image
    rbd-host          pool_name image_name          Find RBD primary storage hosts
    rbd-osd           pool_name image_name          Find RBD primary OSDs
    rbd-size          pool_name image_name          Print RBD image real size
    rbd-all-size      pool_name                     Print all RBD images size (Top first)

    OSD
    ----
    osd-most-used                                   Show the most used OSD (capacity)
    osd-less-used                                   Show the less used OSD (capacity)
    osd-get-ppg       osd_id                        Show all primaries PGS hosted on a OSD
    osd-get-pg        osd_id                        Show all PGS hosted on a OSD

    Objects
    --------
    object-get-host   pool_name object_id           Find object storage hosts (first is primary)


## WHAT ARE THE DEPENDENCIES

You obviously need the Ceph cli toolset binaries (ceph, rados, rbd, osdmaptool) as well as the jq utility which is used to parse json output. JSON parsing is much more efficient and easy to code than sed/grep/awk. The "bc" command is required for the "host-osd-usage" and "host-all-usage"commands.

You also need the proper cephx permissions on both MONs and OSDs/pool you will query.


## HOW TO INSTALL

Usage is pretty straightforward just ensure you have all dependencies installed, clone the git repo

```
git clone https://github.com/gcharot/ceph-lazy.git
```

Copy the ceph-lazy to a PATH directory and ensure the proper permissions are set.
```
cp ceph-lazy/ceph-lazy /usr/local/sbin/
chown root:root /usr/local/sbin/ceph-lazy
chmod u+x /usr/local/sbin/ceph-lazy
```

If you want to enable bash completion you can copy the completion config file.
```
cp ceph-lazy/bash_completion.d/ceph-lazy /etc/bash_completion.d/
```

## HOW TO USE

Simply execute ceph-lazy with no parameter or use the -h option to get the list of options and commands. Using -d as first parameter enable verbose mode (printed on stderr). General syntax usage is :

```
Usage : ceph-lazy [-d | -h] [command] [parameters]
```

## TODO

- Add more error controls
- Find new command ideas
- Optimise query performances when possible
