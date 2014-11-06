# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re
from string import Template as _template
import pickle, config_transporter

def write_config_file(**kwargs):
    '''
    Writes updates to Nagios config file from template.
    '''
    file_dir = kwargs.pop('file_dir', '/usr/local/nagios/etc/')
    template_dir = kwargs.pop('template_dir', '/usr/local/nagios/etc/')
    target_config_file = open(str('%snagios.cfg' % file_dir), 'w')
    template_file_name = str('%snagios-template.cfg' % template_dir)
    with open(template_file_name, 'r') as template_file:
        for line in template_file:
            if re.search('nagios_config_files', line):
                param = _template(line)
                line = param.substitute(nagios_config_files='')
                with open(str('%sintermediate.txt' % template_dir), 'r') as intermediate:
                    for temp_line in intermediate:
                        line = temp_line
                        buf = str(line)
                        target_config_file.write(buf)                        
            else:
                buf = str(line)
                target_config_file.write(buf)
    target_config_file.close()
    return target_config_file.name

def write_config_files(**kwargs):
    '''
    Writes list of VMs to be monitored to text file.
    '''
    vm_dir = kwargs.pop('vm_dir', '/usr/local/nagios/etc/objects/vm/')
    servers = pickle.load(open('/usr/local/nagios/etc/server_list', 'r'))
    [config_transporter.add_file_to_nagios_conf_dir(file_dir=vm_dir, 
                                                    name=server[0],
                                                    vm_ip=server[2]) 
         for server in servers
         if server[0] != u'nagios_test']
    
if __name__ == "__main__":
    config_transporter.write_intermediate_file()
    write_config_files()
    _TARGET_CONFIG_FILE_NAME = write_config_file()
    print(_TARGET_CONFIG_FILE_NAME)
