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


def nagios_plugins_downloaded():
    return cuisine.file_exists("~/nagios-plugins-2.0.3.tar.gz")

@task
def add_nagios_user():
    cuisine.group_ensure('nagios')
    cuisine.user_ensure('nagios',shell='which nologin')
    cuisine.group_user_ensure('nagios','nagios')
    cuisine.dir_ensure('/usr/local/nagios')
    cuisine.dir_ensure('/usr/local/nagios/libexec')
    sudo('chown nagios.nagios /usr/local/nagios')
    sudo('chown -R nagios.nagios /usr/local/nagios/libexec')

@task
def add_nrpe_port():
    cuisine.package_ensure('xinetd')
    sudo('echo "nrpe 5666/tcp" >> /etc/services')

@task
def install_nagios_plugins_from_source():
    cuisine.dir_ensure('/usr/local/src')
    run('cd /usr/local/src')
    if not nagios_plugins_downloaded():
        sudo('wget http://nagios-plugins.org/download/nagios-plugins-2.0.3.tar.gz')
    sudo('tar xzf nagios-plugins-2.0.3.tar.gz')
    sudo('cd ~/nagios-plugins-2.0.3 && ./configure --with-nagios-user=nagios --with-nagios-group=nagios && make && make install')
    
@task
def install_nrpe_plugin_from_source():
    cuisine.package_ensure_apt('libssl-dev')
    cuisine.dir_ensure('/usr/local/src')
    run('cd /usr/local/src')
    if not nagios_plugins_downloaded():
        sudo('wget http://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz')
    sudo('tar xzf nrpe-2.15.tar.gz')
    sudo('cd ~/nrpe-2.15 && ./configure --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu && make && make install')
    sudo('cd ~/nrpe-2.15 && make install-xinetd install-daemon-config')

@task
def configure_xinetd_for_nrpe():
    sed('/etc/xinetd.d/nrpe','only_from       = 127.0.0.1','only_from       = 160.85.4.238,127.0.0.1',use_sudo=True)
    sudo('service xinetd restart')

@task
def install_autoconf():
    put('./remote.py','/usr/local/nagios/etc/nrpe.cfg',use_sudo=True)
    put('./check_memory.sh','/usr/local/nagios/libexec/check_memory.sh',use_sudo=True)
    

execute(add_nagios_user)
execute(add_nrpe_port)    
execute(install_nagios_plugins_from_source)
execute(install_nrpe_plugin_from_source)
execute(configure_xinetd_for_nrpe)
execute(configure_nrpe)