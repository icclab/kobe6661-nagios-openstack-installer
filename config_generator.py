# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re
from string import Template as _template


def write_config_file(**kwargs):
    '''
    Writes a single Nagios config file that represents a VM 
    in the /etc/ directory of the Nagios VM. It uses a template 
    for creating the config file.
    
    Arguments:
    FILE_DIR -- local directory on Nagios server 
    where the VM config resides.
    TEMPLATE_DIR -- local directory on Nagios server 
    where the template resides.
    name -- name of the VM that is configured.
    ip -- IP of the VM that is configured.
    '''
    FILE_DIR=kwargs.pop('FILE_DIR','')
    TEMPLATE_DIR=kwargs.pop('TEMPLATE_DIR','/usr/local/nagios/etc')
    name=kwargs.pop('name','def')
    ip=kwargs.pop('ip','1.1.1.1')
    target_config_file = open(str('%s%s_nagios.cfg' % (FILE_DIR,name)),'w')
    template_file_name=str('%s/vm_template.cfg' % TEMPLATE_DIR)
    with open(template_file_name,'r') as f:
        for line in f:
            if re.search('vm_name',line):
                s = _template(line)
                line = s.substitute(vm_name=name)
            elif re.search('vm_ip',line):
                s = _template(line)
                line = s.substitute(vm_ip=ip)
            buf = str(line)
            target_config_file.write(buf)
    target_config_file.close()
    return target_config_file.name
    
if __name__ == "__main__":
    help(write_config_file)
    #_target_config_file_name = write_config_file(name='test',ip='192.168.0.2')
    #print(_target_config_file_name)