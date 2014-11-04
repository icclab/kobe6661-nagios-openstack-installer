# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:03:31 2014

@author: Konstantin
"""

import config_generator, pickle

def add_file_to_nagios_conf_dir(**kwargs):
    '''
    Adds VM config file to Nagios configuration directory.
    '''
    file_dir = kwargs.pop('file_dir', '/usr/local/nagios/etc/objects/vm/')
    name = kwargs.pop('name', 'test')
    vm_ip = kwargs.pop('vm_ip', '1.1.1.1')
    config_generator.write_config_file(file_dir=file_dir,
                                       name=name,
                                       vm_ip=vm_ip)
#    intermediate=open('~/intermediate.cfg','w')
#    intermediate.write(str('\ncfg_file=%s' % _target_file))
#    intermediate.close()

def write_intermediate_file(**kwargs):
    '''
    Writes list of VMs to be monitored to text file.
    '''
    nagios_dir = kwargs.pop('nagios_dir', '/usr/local/nagios/etc/')
    vm_dir = kwargs.pop('vm_dir', '/usr/local/nagios/etc/objects/vm/')
    servers = pickle.load(open('server_list', 'r'))
    with open(str('%sintermediate.txt' % nagios_dir), 'w') as intermediate:
        [intermediate.write(str('\ncfg_file=%s%s_nagios.cfg' % (vm_dir, server[0]))) 
         for server in servers
         if server[0] != u'nagios_test']

if __name__ == "__main__":
    add_file_to_nagios_conf_dir(file_dir='./vm/',
                                name='test',
                                vm_ip='192.168.0.2')
