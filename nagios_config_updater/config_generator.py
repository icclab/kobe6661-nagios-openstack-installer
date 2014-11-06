# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:00:29 2014

@author: Konstantin
"""

import re
from string import Template as _template


def write_config_file(**kwargs):
    '''
    Writes a single Nagios config file that represents a VM in the /etc/
    directory of the Nagios VM. It uses a template for creating the config
    file.

    Arguments:
        :file_dir: local directory on Nagios server
            where the VM config resides.
        :template_dir: local directory on Nagios server
            where the template resides.
        :name: name of the VM that is configured.
        :vm_ip: IP of the VM that is configured.
'''
    file_dir = kwargs.pop('file_dir', '')
    template_dir = kwargs.pop('template_dir', '/usr/local/nagios/etc')
    name = kwargs.pop('name', 'def')
    vm_ip = kwargs.pop('vm_ip', '1.1.1.1')
    target_config_file = open(str('%s%s_nagios.cfg' % (file_dir, name)), 'w')
    template_file_name = str('%s/vm_template.cfg' % template_dir)
    with open(template_file_name, 'r') as template_file:
        for line in template_file:
            if re.search('vm_name', line):
                param = _template(line)
                line = param.substitute(vm_name=name)
            elif re.search('vm_ip', line):
                param = _template(line)
                line = param.substitute(vm_ip=vm_ip)
            buf = str(line)
            target_config_file.write(buf)
    target_config_file.close()
    return target_config_file.name


if __name__ == "__main__":
    help(write_config_file)
    #_target_config_file_name = write_config_file(name='test',ip='192.168.0.2')
    #print(_target_config_file_name)
