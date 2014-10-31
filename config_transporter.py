# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:03:31 2014

@author: Konstantin
"""

import config_generator, pickle

def add_file_to_nagios_conf_dir(**kwargs):
    FILE_DIR=kwargs.pop('FILE_DIR','/usr/local/nagios/etc/objects/vm/')
    name=kwargs.pop('name','test')
    ip=kwargs.pop('ip','1.1.1.1')
    config_generator.write_config_file(FILE_DIR=FILE_DIR,
                                                    name=name,
                                                    ip=ip)
#    intermediate=open('~/intermediate.cfg','w')
#    intermediate.write(str('\ncfg_file=%s' % _target_file))
#    intermediate.close()  

def write_intermediate_file(**kwargs):
    NAGIOS_DIR=kwargs.pop('NAGIOS_DIR','/usr/local/nagios/etc/')
    VM_DIR=kwargs.pop('VM_DIR','/usr/local/nagios/etc/objects/vm/')
    servers = pickle.load(open('server_list','r'))
    with open(str('%sintermediate.txt' % NAGIOS_DIR),'w') as f:
        [f.write(str('\ncfg_file=%s%s_nagios.cfg' % (VM_DIR,server[0]))) for server in servers]
            
        
    
if __name__ == "__main__":
    add_file_to_nagios_conf_dir(FILE_DIR='./vm/',
                                name='test',
                                ip='192.168.0.2')