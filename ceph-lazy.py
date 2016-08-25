#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import json
import optparse

VERSION="1.1.2"

def main():
    if len(sys.argv) == 1:  
        sys.argv.append("-h")  
    if sys.argv[1] == '-h' or sys.argv[1] == 'help':
        help()
    if sys.argv[1] == 'host-get-osd':
        if len(sys.argv) == 3:
            for osd in list_osd_from_host( sys.argv[2] ):
                print osd
        else:
            print "host-get-osd <hostname>                    列出节点上的所有的osd."
    if sys.argv[1] == 'host-get-nodes':
        if len(sys.argv) == 2:
            for node in list_all_nodes():
                print node
        else:
            print "list_all_nodes                             列出所有的存储主机节点"
    if sys.argv[1] == 'host-osd-usage':
        if len(sys.argv) == 3:
            for item in show_host_osd_usage(sys.argv[2],False):
                print item
        elif len(sys.argv) == 4 and sys.argv[3] == "detail":
            for item in  show_host_osd_usage(sys.argv[2],True):
                print item
        else:
            print "host-osd-usage    hostname       [detail]               列出指定存储节点上的存储使用的情况(detail看详细信息)"
    if sys.argv[1] == 'host-all-usage':
        if len(sys.argv) == 2:
            list_all_nodes_osd_usage(False)
        elif len(sys.argv) == 3 and sys.argv[2] == "detail":
            list_all_nodes_osd_usage(True)
        else:
            print "host-all-usage                   [detail]               列出所有存储节点上的存储使用的情况(detail看详细信息)"

    if sys.argv[1] == 'pg-get-host':
        if len(sys.argv) == 3:
            try:
                for item in  find_host_from_pg(sys.argv[2]):
                    print item
            except:
                print "Nothing out put ,check your pg id!"
        else:
            print "pg-get-host       pgid                                  列出PG所在的节点(first is primary)"

    if sys.argv[1] == 'pg-most-write':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-most-write" )           
        else:
            print "pg-most-write               列出写操作最多的PG ( operations number)"

    if sys.argv[1] == 'pg-less-write':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-less-write" )
        else:
            print "pg-less-write               列出写操作最少的PG ( operations number)"
    if sys.argv[1] == 'pg-most-write-kb':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-most-write-kb" )
        else:
            print "pg-most-write-kb               列出写操作最多的PG (data written) "
    if sys.argv[1] == 'pg-less-write-kb':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-less-write-kb" )
        else:
            print "pg-less-write-kb               列出写操作最少的PG (data written) "
    if sys.argv[1] == 'pg-most-read':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-most-read" )
        else:
            print "pg-most-read               列出读操作最多的PG (operations number) "

    if sys.argv[1] == 'pg-less-read':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-less-read" )
        else:
            print "pg-less-read               列出读操作最少的PG (operations number) "

    if sys.argv[1] == 'pg-most-read-kb':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-most-read-kb" )
        else:
            print "pg-most-read-kb               列出读操作最多的PG (data written) "
    if sys.argv[1] == 'pg-less-read-kb':
        if len(sys.argv) == 2:
            print pg_stat_query( "pg-less-read-kb" )
        else:
            print "pg-less-read-kb               列出读操作最少的PG (data written) "

    if sys.argv[1] == 'pg-empty':
        if len(sys.argv) == 2:
            for item in find_empty_pg():
                print item
        else:
            print "pg-empty                        列出空的PG (没有存储对象) "

    if sys.argv[1] == 'rbd-prefix':
        if len(sys.argv) == 4:
            try:
                print get_rbd_prefix(sys.argv[2],sys.argv[3])    
            except:
                print "no data!"
        else:
            print "rbd-prefix        pool_name image_name         列出RBD的prefix"

    if sys.argv[1] == 'rbd-count':
        if len(sys.argv) == 4:
            try:
                print count_rbd_object(sys.argv[2],sys.argv[3])
            except:
                print "no data!"
        else:
            print "rbd-count        pool_name image_name         列出RBD的count"



#
# List osd from host(修改函数为传参数进去的形式，直接在函数调用的时候输入命令行传递的参数，方便其他函数调用)
#
def list_osd_from_host( hostname ):
    osdlist = []
    list_osd_tree = commands.getoutput('ceph osd tree --format json-pretty 2>/dev/null')
    json_str = json.loads(list_osd_tree)
    for item in  json_str["nodes"]:
        if item['name'] == hostname and item['type'] == 'host':
            item['children'].sort()
            for osd in item['children']:
                osdlist.append(osd)
    return osdlist
#
# List all OSD nodes
#

def list_all_nodes() :
    nodelist = []
    list_all_host = commands.getoutput('ceph osd tree --format json-pretty 2>/dev/null')	
    try:
        json_str = json.loads(list_all_host)
    except:
        print "no  data"
    for item in  json_str["nodes"]:
        if item['type'] == 'host':
            nodelist.append(item['name'])
    return nodelist
            
#
#Print Total OSD usage of a particular storage host
#
def show_host_osd_usage(hostname,detail):
    osd_size_kb_list=[]
    osd_used_kb_list=[]
    osd_available_kb_list=[]
    result_list=[]
    list_host_osds = commands.getoutput('ceph  pg dump  osds --format json 2>/dev/null')
    json_str = json.loads(list_host_osds)
    for osdnum in list_osd_from_host(hostname):
        for item in json_str:
            if item['osd'] == osdnum:
                osd_size_kb_list.append(item['kb'])
                osd_used_kb_list.append(item['kb_used'])
                osd_available_kb_list.append(item['kb_avail'])
                if  detail == True:
                    OSDsinglesize = item['kb']/1024/1024.0
                    OSDsingleused = item['kb_used']/1024/1024.0
                    OSDsingleavailable = item['kb_avail']/1024/1024.0
                    result_list.append("OSD:"+ str(osdnum) + " | " + "Size:" +str(float('%.1f'%OSDsinglesize)) +"GB"+ " | " +"Used:" + str(float('%.1f'%OSDsingleused))+ "GB" + " | " +"Available:" + str(float('%.1f'%OSDsingleavailable))+"GB")
    OSDsum = sum(osd_size_kb_list)/1024/1024.0
    OSDused = sum(osd_used_kb_list)/1024/1024.0
    OSDavailable = sum(osd_available_kb_list)/1024/1024.0
    result_list.append( "Host"+":"+str(hostname)+" | " + "OSDs:"+ str(len(osd_size_kb_list))+" | "+ "Total_Size:"+str(float('%.1f'%OSDsum))+"GB"+" | "+ "Total_Used:"+ str(float('%.1f'%OSDused)) +"GB"+" | "+"Total_Available:" + str(float('%.1f'%OSDavailable)) + "GB")
    return result_list

#
# Print Total OSD usage of all nodes
#
def list_all_nodes_osd_usage(detail):
    for node in list_all_nodes():
        print "----------------------------------------------"
        for item in show_host_osd_usage(node,detail):
            print item

#
#  Print the host that hosts a specific PG
#

def find_host_from_pg(pgname):
    result_list=[]
    list_pg = commands.getoutput('ceph  pg %s  query 2>/dev/null' %pgname )
    try:
        json_str = json.loads(list_pg)
    except:
        print "can not get pg data !"
    else:
        for item in  json_str["up"]:
            osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %item )
            json_str1 = json.loads(osd_localtion)
            result_list.append( "OSD:"+"osd."+str(item)+ " | "+ "Host :"+ json_str1["crush_location"]["host"])
        return result_list


#
#  Query PG stats
#
def pg_stat_query(arg):
    list_pgs = commands.getoutput('ceph  pg dump  pgs --format json 2>/dev/null')
    json_str = json.loads(list_pgs)
#    print json_str
    if arg == "pg-most-write":
        max_num_write_item = max(json_str, key=lambda x:x['stat_sum']["num_write"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(max_num_write_item["acting_primary"]) ) 
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)
    if arg == "pg-less-write":
        min_num_write_item = min(json_str, key=lambda x:x['stat_sum']["num_write"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(min_num_write_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(min_num_write_item["pgid"])+" | "+"OSD:osd."+str(min_num_write_item["acting_primary"])+" | "+"Host:"+str(host)        
    if arg == "pg-most-write-kb":
        max_num_write_item = max(json_str, key=lambda x:x['stat_sum']["num_write_kb"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(max_num_write_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)
    if arg == "pg-less-write-kb":
        min_num_write_item = min(json_str, key=lambda x:x['stat_sum']["num_write_kb"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(min_num_write_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)
    if arg == "pg-most-read":
        max_num_read_item = max(json_str, key=lambda x:x['stat_sum']["num_read"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(max_num_read_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)
    if arg == "pg-less-read":
        min_num_read_item = max(json_str, key=lambda x:x['stat_sum']["num_read"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(min_num_read_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)
    if arg == "pg-most-read-kb":
        max_num_read_item = max(json_str, key=lambda x:x['stat_sum']["num_read_kb"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(max_num_read_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)

    if arg == "pg-less-read-kb":
        min_num_read_item = min(json_str, key=lambda x:x['stat_sum']["num_read_kb"])
        osd_localtion = commands.getoutput('ceph  osd find  %s  --format json 2>/dev/null' %str(min_num_read_item["acting_primary"]) )
        json_str1 = json.loads(osd_localtion)
        host=json_str1["crush_location"]["host"]
        return  "PG:"+str(max_num_write_item["pgid"])+" | "+"OSD:osd."+str(max_num_write_item["acting_primary"])+" | "+"Host:"+str(host)


def find_empty_pg():
    null_pg_list=[]
    null_pg = commands.getoutput('ceph pg dump pgs --format json 2>/dev/null' )
    json_str = json.loads(null_pg)
    for item in json_str:
        if item['stat_sum']['num_objects'] == 0:
            null_pg_list.append(item['pgid'])
    return null_pg_list



#
#  Return RBD prefix from image name
#
def get_rbd_prefix(poolname,imagename):
    rbd_info = commands.getoutput('rbd --image %s -p %s info --format json 2> /dev/null' %(imagename,poolname) )
    try:
        json_str = json.loads(rbd_info)
    except:
        print "no rbd data found!check your poolname and imagename!"
    return json_str["block_name_prefix"]

#
#  Return RBD count from image name
#
def count_rbd_object(poolname,imagename):
    rbd_prefix=get_rbd_prefix(poolname,imagename)
    nb_obj=commands.getoutput('rados -p  %s  ls|grep %s|wc -l  2>/dev/null' %(poolname,rbd_prefix) )
    return """
    RBD image %s/%s has prefix %s; now couning objects...
    count: %s    
    """  %(poolname,imagename,rbd_prefix,nb_obj)

#    rbd_info = commands.getoutput('rbd --image %s -p %s info --format json 2> /dev/null' %(imagename,poolname) )
#    try:
#        json_str = json.loads(rbd_info)
#    except:
#        print "no rbd data found!check your poolname and imagename!"
#    return json_str["block_name_prefix"]

    


#
# check requirements for this script
#
def check_requirements():
    (checkceph, output) = commands.getstatusoutput('ceph --version >/dev/null 2>&1')
    (checkrados, output) = commands.getstatusoutput('rados --version >/dev/null 2>&1')
    (checkrbd, output) = commands.getstatusoutput('rbd --version >/dev/null 2>&1')
    (checkosdmaptool, output) = commands.getstatusoutput('osdmaptool --version >/dev/null 2>&1')
    checkstatus = checkceph or checkrados or checkrbd or checkosdmaptool
    if checkstatus != 0:
        print 'some command not found!'
        print commands.getoutput('ceph --version 1 > /dev/null')
        print commands.getoutput('rados --version 1 > /dev/null')
        print commands.getoutput('rbd --version 1 > /dev/null')
        print commands.getoutput('osdmaptool --version 1 > /dev/null')

#
#print help info
#

def help():
    print """Usage : ceph-lazy [-d | -h] [command] [parameters]
Ceph complex quering tool - Version $VERSION
OPTIONS
========
    -d          Activate debug mode
    -h          Print help
COMMANDS
=========
    --------
   |  Host  |
    --------
    host-get-osd      hostname                      列出节点上的所有的OSD.
    host-get-nodes                                  列出所有的存储节点.
    host-osd-usage    hostname     [detail]         列出存储节点上的存储使用的情况(detail看详细信息)
    host-all-usage                 [detail]         列出指定存储节点上的存储使用的情况(detail看详细信息)
    Placement groups
    ------------------
   | Placement groups |
    ------------------
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
    --------
   |   RBD  |
    --------
    rbd-prefix        pool_name image_name          Return RBD image prefix
    rbd-count         pool_name image_name          Count number of objects in a RBD image
    rbd-host          pool_name image_name          Find RBD primary storage hosts
    rbd-osd           pool_name image_name          Find RBD primary OSDs
    rbd-size          pool_name image_name          Print RBD image real size
    rbd-all-size      pool_name                     Print all RBD images size (Top first)
    --------
   |   OSD  |
    --------
    osd-most-used                                   Show the most used OSD (capacity)
    osd-less-used                                   Show the less used OSD (capacity)
    osd-get-ppg       osd_id                        Show all primaries PGS hosted on a OSD
    osd-get-pg        osd_id                        Show all PGS hosted on a OSD
    Objects
    --------
    object-get-host   pool_name object_id           Find object storage hosts (first is primary)
"""

if __name__ == '__main__':
    check_requirements()
    main()
