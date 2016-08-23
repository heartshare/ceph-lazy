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
            for osd in list_osd_from_host():
                print osd
        else:
            print "host-get-osd <hostname>                    列出节点上的所有的osd."
    if sys.argv[1] == 'list_all_nodes':
        if len(sys.argv) == 2:
            list_all_nodes()
        else:
            print "list_all_nodes                             列出所有的存储主机节点"
    if sys.argv[1] == 'host-osd-usage':
        if len(sys.argv) == 3:
            show_host_osd_usage()
        elif len(sys.argv) == 4 and sys.argv[3] == "detail":
            show_host_osd_usage()
        else:
            print "host-osd-usage    hostname       [detail]               列出存储节点上的存储使用的情况(detail看详细信息)"

#
# List osd from host
#
def list_osd_from_host():
    osdlist = []
    list_osd_tree = commands.getoutput('ceph osd tree --format json-pretty 2>1')
    json_str = json.loads(list_osd_tree)
    for item in  json_str["nodes"]:
        if item['name'] == sys.argv[2] and item['type'] == 'host':
            item['children'].sort()
            for osd in item['children']:
                osdlist.append(osd)
    return osdlist
#
# List all OSD nodes
#

def list_all_nodes() :
    list_all_host = commands.getoutput('ceph osd tree --format json-pretty 2>1')	
    json_str = json.loads(list_all_host)
    for item in  json_str["nodes"]:
        if item['type'] == 'host':
            print item['name']
            

#
#Print Total OSD usage of a particular storage host
#
def show_host_osd_usage():
    
    osd_size_kb_list=[]
    osd_used_kb_list=[]
    osd_available_kb_list=[]
    list_host_osds = commands.getoutput('ceph  pg dump  osds --format json 2>1')
    json_str = json.loads(list_host_osds)
    for osdnum in list_osd_from_host():
        for item in json_str:
            if item['osd'] == osdnum:
                osd_size_kb_list.append(item['kb'])
                osd_used_kb_list.append(item['kb_used'])
                osd_available_kb_list.append(item['kb_avail'])
                if  len(sys.argv) == 4:
                    OSDsinglesize = item['kb']/1024/1024.0
                    OSDsingleused = item['kb_used']/1024/1024.0
                    OSDsingleavailable = item['kb_avail']/1024/1024.0
                    print "OSD:"+ str(osdnum) + " | " + "Size:" +str(float('%.1f'%OSDsinglesize)) +"GB"+ " | " +"Used:" + str(float('%.1f'%OSDsingleused))+ "GB" + " | " +"Available:" + str(float('%.1f'%OSDsingleavailable))+"GB"

    OSDsum = sum(osd_size_kb_list)/1024/1024.0
    OSDused = sum(osd_used_kb_list)/1024/1024.0
    OSDavailable = sum(osd_available_kb_list)/1024/1024.0
    print "Host"+":"+str(sys.argv[2])+" | " + "OSDs:"+ str(len(osd_size_kb_list))+" | "+ "Total_Size:"+str(float('%.1f'%OSDsum))+"GB"+" | "+ "Total_Used:"+ str(float('%.1f'%OSDused)) +"GB"+" | "+"Total_Available:" + str(float('%.1f'%OSDavailable)) + "GB"

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
    host-all-usage                                  Show total OSD space usage of each nodes (-d for details)
    Placement groups
    --------
   |   PG   |
    --------
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
