#!/usr/bin/env python
#
# Vitaly Nikolenko
# vnik@hashcrack.org

import subprocess
import re
import pdb
import sys

def parse(intf, my_list):
    p = subprocess.Popen(['/sbin/iwlist', intf, 'scan'], stdout=subprocess.PIPE)
    
    # some hideous parsing
    ap_list = []
    signal = None
    essid = None
    for x in p.stdout.readlines():
       x = x.strip()
       if x.find('Cell') != -1:
           if essid is not None:
               ap_list.append((essid, quality))
           essid = None
    
       if x.find('Quality') != -1:
          m = re.match(r'.*?=(-\d\d) dBm$', x) 
          quality = m.group(1)
    
       if x.find('ESSID') != -1:
          _,_essid = x.split(':')
          essid = _essid[1:-1]
          if essid not in my_list:
              essid = None

    ap_list.sort(key=lambda x: int(x[1]), reverse=True)
    return ap_list

def to_find(file_path):
    f = open(file_path, 'r')
    ap_list = [x.strip() for x in f.readlines()]
    f.close()
    return ap_list

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage %s int_antenna_intf ext_antenna_intf essid_file' % sys.argv[0]
        sys.exit(-1)

    my_list = to_find(sys.argv[3])
    int_list = parse(sys.argv[1], my_list)
    ext_list = parse(sys.argv[2], my_list)

    # awesomely inefficient
    print "AP_NAME                  INT_SIGNAL      EXT_SIGNAL"
    for ap in my_list:
        int_sig = 'None'
        ext_sig = 'None'
        
        for tmp in int_list:
            if ap == tmp[0]:
                int_sig = tmp[1]
        
        for tmp in ext_list:
            if ap == tmp[0]:
                ext_sig = tmp[1]
        print "%s%s%s             %s" % (ap, (25-len(ap))*' ', int_sig, ext_sig)
