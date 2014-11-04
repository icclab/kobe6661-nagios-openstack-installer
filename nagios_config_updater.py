# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re
from string import Template as _template


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
    
if __name__ == "__main__":
    _TARGET_CONFIG_FILE_NAME = write_config_file()
    print(_TARGET_CONFIG_FILE_NAME)
