# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 12:41:21 2014

@author: Konstantin
"""
import cuisine, configparser, pickle
from fabric.api import env, execute, task, run, sudo, put, parallel
from fabric.contrib.files import sed

config = configparser.ConfigParser()
config.read('/usr/local/nagios/config.ini')

HOST_LIST = pickle.load(open('/usr/local/nagios/etc/server_list', 'r'))

nagios_server = dict(config['NAGIOS_SERVER'])
nagios_server_name = str(nagios_server['nagios_server.name'])

ssh_credentials = dict(config['SSH_CREDENTIALS'])
ssh_user = str(ssh_credentials['nagios_ssh.user'])
ssh_password = str(ssh_credentials['nagios_ssh.password'])
ssh_key_filename = str(ssh_credentials['nagios_ssh.remote_key_filename'])

#env.hosts = [host[2] for host in host_list if host[0] != u'nagios_test']
env.hosts = [host[2] for host in HOST_LIST if host[0] != nagios_server_name]
env.user = ssh_user
env.password = ssh_password
env.key_filename = ssh_key_filename
print(env.key_filename)

@parallel(pool_size=5)
@task
def install_prerequisites():
    '''
    Installs prerequisites on monitored VMs.
    '''
    cuisine.package_ensure('gcc')
    cuisine.package_ensure('build-essential')
    cuisine.package_ensure('libssl-dev')
    cuisine.package_ensure('iptables-persistent')

def nagios_plugins_downloaded():
    '''
    Checks if Nagios plugins are downloaded to VMs.
    '''
    return cuisine.file_exists("~/nagios-plugins-2.0.3.tar.gz")

def nrpe_plugins_downloaded():
    '''
    Checks if NRPE plugins are downloaded to VMs.
    '''
    return cuisine.file_exists("~/nrpe-2.15.tar.gz")

@parallel(pool_size=5)
@task
def add_nagios_user():
    '''
    Adds Nagios user and groups to VMs and sets the right permissions.
    '''
    cuisine.group_ensure('nagios')
    cuisine.user_ensure('nagios')
    cuisine.group_user_ensure('nagios', 'nagios')
    sudo('mkdir -p /usr/local/nagios')
    sudo('mkdir -p /usr/local/nagios/libexec')
    cuisine.dir_ensure('/usr/local/nagios')
    cuisine.dir_ensure('/usr/local/nagios/libexec')
    sudo('chown nagios.nagios /usr/local/nagios')
    sudo('chown -R nagios.nagios /usr/local/nagios/libexec')

@parallel(pool_size=5)
@task
def add_nrpe_port():
    '''
    Configures settings to permit incoming NRPE connections on port 5666.
    '''
    cuisine.package_ensure('xinetd')
    sudo('echo "nrpe 5666/tcp" >> /etc/services')
    sudo('iptables -A INPUT -p tcp --dport 5666 -j ACCEPT')

@parallel(pool_size=5)
@task
def install_nagios_plugins_from_source():
    '''
    Downloads Nagios plugins source code and installs Nagios plugins on VMs.
    '''
    cuisine.dir_ensure('/usr/local/src')
    run('cd /usr/local/src')
    if not nagios_plugins_downloaded():
        sudo('wget http://nagios-plugins.org/download/nagios-plugins-2.0.3.tar.gz')
    sudo('tar xzf nagios-plugins-2.0.3.tar.gz')
    sudo('cd ~/nagios-plugins-2.0.3 && ./configure --with-nagios-user=nagios --with-nagios-group=nagios && make && make install')

@parallel(pool_size=5)
@task
def install_nrpe_plugin_from_source():
    '''
    Downloads NRPE plugin source code and installs NRPE plugins on VMs.
    '''
    cuisine.dir_ensure('/usr/local/src')
    run('cd /usr/local/src')
    if not nrpe_plugins_downloaded():
        sudo('wget http://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz')
    sudo('tar xzf nrpe-2.15.tar.gz')
    sudo('cd ~/nrpe-2.15 && ./configure --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu && make all && make install-plugin')
    sudo('cd ~/nrpe-2.15 && make install-daemon && make install-daemon-config && make install-xinetd')

@parallel(pool_size=5)
@task
def configure_xinetd_for_nrpe():
    '''
    Configures Xinet daemon to accept connections from Nagios VM.
    '''
    sed('/etc/xinetd.d/nrpe', 'only_from       = 127.0.0.1', 'only_from       = 160.85.4.238 10.10.2.56 127.0.0.1', use_sudo=True)
    sudo('service xinetd restart')

@parallel(pool_size=5)
@task
def configure_nrpe():
    '''
    Connfigures NRPE on VMs to perform service checks remotely.
    '''
    put('/usr/local/nagios/etc/nrpe.cfg', '/usr/local/nagios/etc/nrpe.cfg', use_sudo=True)
    sudo('chown -R nagios.nagios /usr/local/nagios/etc')
    sudo('chown -R nagios.nagios /usr/local/nagios/etc/nrpe.cfg')
    put('/usr/local/nagios/libexec/check_memory.sh', '/usr/local/nagios/libexec/check_memory.sh', use_sudo=True)
    sudo('chown -R nagios.nagios /usr/local/nagios/libexec/check_memory.sh')
    sudo('chmod 0755 /usr/local/nagios/libexec/check_memory.sh')

execute(install_prerequisites)
execute(add_nagios_user)
execute(add_nrpe_port)
execute(install_nagios_plugins_from_source)
execute(install_nrpe_plugin_from_source)
execute(configure_xinetd_for_nrpe)
execute(configure_nrpe)
