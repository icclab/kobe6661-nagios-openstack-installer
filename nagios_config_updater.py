# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re, os
from string import Template as _template


def write_config_file(**kwargs):
    FILE_DIR=kwargs.pop('FILE_DIR','')
    TEMPLATE_DIR=kwargs.pop('TEMPLATE_DIR','/usr/local/nagios/etc/')
    target_config_file = open(str('%s/nagios.cfg' % FILE_DIR),'w')
    template_file_name=str('%s/nagios-template.cfg' % TEMPLATE_DIR)
    with open(template_file_name,'r') as f:
        for line in f:
            if re.search('nagios_config_files',line):
                s = _template(line)
                line = s.substitute(nagios_config_files='')
                with open(str('%sintermediate.txt' % TEMPLATE_DIR),'r') as i:
                    for temp_line in i:
                        line = temp_line
                        buf = str(line)
                        target_config_file.write(buf)                        
            else:
                buf = str(line)
                target_config_file.write(buf)
    target_config_file.close()
    return target_config_file.name
    
if __name__ == "__main__":
    _target_config_file_name = write_config_file()
    print(_target_config_file_name)