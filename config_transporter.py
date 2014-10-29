# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:03:31 2014

@author: Konstantin
"""

import config_generator

def add_file_to_nagios_conf_dir(**kwargs):
    NAGIOS_DIR=kwargs.pop('NAGIOS_DIR','/usr/local/nagios/etc/')
    FILE_DIR=kwargs.pop('FILE_DIR','/usr/local/nagios/etc/objects/vm/')
    name=kwargs.pop('name','test')
    ip=kwargs.pop('ip','1.1.1.1')
    _target_file=config_generator.write_config_file(FILE_DIR=FILE_DIR,
                                                    name=name,
                                                    ip=ip)
    
    with open(str('%snagios.cfg' % NAGIOS_DIR),'a') as f:
        f.write(str('\ncfg_file=%s' % _target_file))
        
    
if __name__ == "__main__":
    add_file_to_nagios_conf_dir(NAGIOS_DIR='',
                                FILE_DIR='./vm/',
                                name='test',
                                ip='192.168.0.2')