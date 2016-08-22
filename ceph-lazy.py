#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import commands
import json


VERSION="1.1.2"


def main():
	
	if sys.argv[1] == '-h' or sys.argv[1] == 'help':
		help()
	if sys.argv[1] == 'host-get-osd':
		list_osd_from_host()


#
# list osd from host
#
def list_osd_from_host():
	if len(sys.argv) <= 2:
		print "more args"
	list_osd_tree = commands.getoutput('ceph osd tree --format json-pretty')
	json_str = json.loads(list_osd_tree)
	for i in  json_str["nodes"]:
			if i['name'] == sys.argv[2]:
		       		 i['children'].sort()
				 for a in i['children']:
					print a


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
    host-get-osd      hostname                      List all OSD IDs attached to a particular node.
    host-get-nodes                                  List all storage nodes.
    host-osd-usage    hostname                      Show total OSD space usage of a particular node (-d for details).
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
