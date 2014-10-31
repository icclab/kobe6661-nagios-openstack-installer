# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 12:41:21 2014

@author: Konstantin
"""
import cuisine, pickle
from fabric.api import env, execute, task, run, sudo, put
from fabric.contrib.files import sed

host_list = pickle.load(open('server_list','r'))

#env.hosts = [host[2] for host in host_list if host[0] != u'nagios_test']
env.hosts=['160.85.4.238']
env.user = 'ubuntu'
env.password = 'Ekbn1980!'
env.key_filename = 'C:\\Users\\Konstantin\\.ssh\\id_rsa'
print(env.key_filename)

@task
def install_prerequisites():
    cuisine.package_ensure('python-dev')
    cuisine.package_ensure('python-pip')
    sudo('pip install python-keystoneclient')
    sudo('pip install python-novaclient')
    sudo('pip install fabric')
    sudo('pip install cuisine')

@task
def install_files():
    put('./remote.py','/usr/local/nagios/etc/remote.py',use_sudo=True)
    put('./config_generator.py','/usr/local/nagios/etc/config_generator.py',use_sudo=True)
    put('./config_transporter.py','/usr/local/nagios/etc/config_transporter.py',use_sudo=True)
    put('./vm_list_extractor.py','/usr/local/nagios/etc/vm_list_extractor.py',use_sudo=True)
    put('./nagios_config_updater.py','/usr/local/nagios/etc/nagios_config_updater.py',use_sudo=True)
    put('./vm_template.cfg','/usr/local/nagios/etc/vm_template.cfg',use_sudo=True)
    put('./commands.cfg','/usr/local/nagios/etc/objects/commands.cfg',use_sudo=True)
    put('./nagios-template.cfg','/usr/local/nagios/etc/nagios-template.cfg',use_sudo=True)
    put('./check_memory.sh','/usr/local/nagios/libexec/check_memory.sh',use_sudo=True)
    
@task
def update_configuration():
    sudo('mkdir -p /usr/local/nagios/etc/objects/vm')
    sudo('python /usr/local/nagios/etc/vm_list_extractor.py')

execute(install_prerequisites)
execute(install_files)
execute(update_configuration)

