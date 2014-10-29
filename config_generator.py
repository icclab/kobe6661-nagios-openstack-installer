# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re, os
from string import Template as _template


def write_config_file(**kwargs):
    FILE_DIR=kwargs.pop('FILE_DIR','')
    name=kwargs.pop('name','def')
    ip=kwargs.pop('ip','1.1.1.1')
    target_config_file = open(str('%s%s_nagios.cfg' % (FILE_DIR,name)),'w')
    template_file_name=str('%s/vm_template.cfg' % os.curdir)
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
    _target_config_file_name = write_config_file(name='test',ip='192.168.0.2')
    print(_target_config_file_name)