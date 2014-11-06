# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 12:41:21 2014

@author: Konstantin
"""
import cuisine, configparser
from fabric.api import env, execute, task, sudo, put
#from fabric.contrib.files import sed

config = configparser.ConfigParser()
config.read('../config.ini')

nagios_server = dict(config['NAGIOS_SERVER'])
nagios_server_ip = str(nagios_server['nagios_server.ip'])
nagios_server_user = str(nagios_server['nagios_server.user'])
nagios_server_password = str(nagios_server['nagios_server.user'])

ssh_credentials = dict(config['SSH_CREDENTIALS'])
ssh_user = str(ssh_credentials['nagios_ssh.user'])
ssh_password = str(ssh_credentials['nagios_ssh.password'])
ssh_key_filename = str(ssh_credentials['nagios_ssh.key_filename'])
ssh_remote_key_filename = str(ssh_credentials['nagios_ssh.remote_key_filename'])
ssh_public_key_filename = str(ssh_credentials['nagios_ssh.public_key_filename'])
ssh_remote_public_key_filename = str(ssh_credentials['nagios_ssh.remote_public_key_filename'])

env.hosts = [nagios_server_ip]
env.user = ssh_user
env.password = ssh_password
env.key_filename = ssh_key_filename
print(env.key_filename)

@task
def install_prerequisites():
    '''
    Installs Python packages required to pocess automatic Nagios config
    upates on Nagios VM.
    '''
    cuisine.package_ensure('python-dev')
    cuisine.package_ensure('python-pip')
    sudo('pip install python-keystoneclient')
    sudo('pip install python-novaclient')
    sudo('pip install ecdsa')
    sudo('pip install fabric')
    sudo('pip install cuisine')
    sudo('pip install configparser')

@task
def install_files():
    '''
    Installs Python scripts and files required for Nagios autoconfiguration on
    Nagios VM.
    '''
    sudo('touch /usr/local/nagios/etc/server_list')
    sudo(str('chown %s.%s /usr/local/nagios/etc/server_list' % (ssh_user,ssh_user)))
    sudo('chmod 0644 /usr/local/nagios/etc/server_list')
    cuisine.file_ensure('/usr/local/nagios/etc/server_list')
    put('../config.ini', '/usr/local/nagios/config.ini', use_sudo=True)
    put('../vm_list_extractor/vm_list_extractor.py', '/usr/local/nagios/etc/vm_list_extractor.py', use_sudo=True)
    put('../openstack_vms_nrpe_config/openstack_vms_nrpe_config.py', '/usr/local/nagios/etc/remote.py', use_sudo=True)
    put('../openstack_vms_nrpe_config/nrpe.cfg', '/usr/local/nagios/etc/nrpe.cfg', use_sudo=True)
    put('../openstack_vms_nrpe_config/check_memory.sh', '/usr/local/nagios/libexec/check_memory.sh', use_sudo=True)
    put('../nagios_config_updater/config_generator.py', '/usr/local/nagios/etc/config_generator.py', use_sudo=True)
    put('../nagios_config_updater/config_transporter.py', '/usr/local/nagios/etc/config_transporter.py', use_sudo=True)
    put('../nagios_config_updater/nagios_config_updater.py', '/usr/local/nagios/etc/nagios_config_updater.py', use_sudo=True)
    put('../nagios_config_updater/vm_template.cfg', '/usr/local/nagios/etc/vm_template.cfg', use_sudo=True)
    put('../nagios_config_updater/nagios-template.cfg', '/usr/local/nagios/etc/nagios-template.cfg', use_sudo=True)
    put('./commands.cfg', '/usr/local/nagios/etc/objects/commands.cfg', use_sudo=True)    
    put(ssh_key_filename, ssh_remote_key_filename, use_sudo=True)
    put(ssh_public_key_filename, ssh_remote_public_key_filename, use_sudo=True)
    sudo(str('chmod 0600 %s'%(ssh_remote_key_filename)))

@task
def update_configuration():
    '''
    Extracts list of VMs to be monitored by Nagios. Configures the VMs to be
    monitored by SSH-connecting into these VMs via Nagios VM and remotely
    installiung the required packages.
    '''
    sudo('mkdir -p /usr/local/nagios/etc/objects/vm')
    sudo('python /usr/local/nagios/etc/vm_list_extractor.py')
    sudo('python /usr/local/nagios/etc/remote.py')
    sudo('python /usr/local/nagios/etc/nagios_config_updater.py')
    sudo('service nagios restart')

execute(install_prerequisites)
execute(install_files)
execute(update_configuration)

