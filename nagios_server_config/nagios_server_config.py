# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 12:41:21 2014

@author: Konstantin
"""
import cuisine, configparser
from fabric.api import env, execute, task, run, sudo, put
#from fabric.contrib.files import sed

# HOST_LIST = pickle.load(open('server_list', 'r'))
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

env.hosts = [nagios_server_ip]
env.user = ssh_user
env.password = ssh_password
env.key_filename = ssh_key_filename
print(env.key_filename)

def nagios_downloaded():
    '''
    Checks if Nagios is downloaded to VM.
    '''
    return cuisine.file_exists("~/nagios-3.4.1.tar.gz")

def nagios_plugins_downloaded():
    '''
    Checks if Nagios plugins are downloaded to VM.
    '''
    return cuisine.file_exists("~/nagios-plugins-2.0.3.tar.gz")

def nrpe_plugins_downloaded():
    '''
    Checks if NRPE plugins are downloaded to VM.
    '''
    return cuisine.file_exists("~/nrpe-2.15.tar.gz")

@task
def add_nagios_user():
    '''
    Adds Nagios user and group and sets correct file permissions.
    '''
    cuisine.group_ensure('nagcmd')
    cuisine.group_ensure('nagios')
    cuisine.user_ensure('nagios')
    cuisine.group_user_ensure('nagios', 'nagios')
    cuisine.group_user_ensure('nagcmd', 'nagios')
    cuisine.user_ensure('www-data')
    cuisine.group_user_ensure('nagcmd', 'www-data')
    sudo('mkdir -p /usr/local/nagios')
    sudo('mkdir -p /usr/local/nagios/libexec')
    cuisine.dir_ensure('/usr/local/nagios')
    cuisine.dir_ensure('/usr/local/nagios/libexec')
    sudo('chown nagios.nagcmd /usr/local/nagios')
    sudo('chown -R nagios.nagcmd /usr/local/nagios/libexec')

@task
def install_prerequisites():
    '''
    Installs prerequisites for running Nagios on VM.
    '''
    cuisine.package_ensure('apache2')
    cuisine.package_ensure('libapache2-mod-php5')
    cuisine.package_ensure('build-essential')
    cuisine.package_ensure('libgd2-xpm-dev')
    cuisine.package_ensure('libssl-dev')

@task
def install_nagios_from_source():
    '''
    Downloads Nagios source code and installs Nagios on VM.
    '''
    cuisine.dir_ensure('/usr/local/src')
    sudo('mkdir -p /etc/httpd/conf.d/')
    cuisine.dir_ensure('/etc/httpd/conf.d/')
    run('cd /usr/local/src')
    if not nagios_downloaded():
        sudo('wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.4.1.tar.gz')
    sudo('tar xzf nagios-3.4.1.tar.gz')
    sudo('cd ~/nagios && ./configure --with-command-group=nagcmd && make all && make install')
    sudo('cd ~/nagios && make install-init && make install-config && make install-commandmode')
    sudo('cd ~/nagios && make install-webconf')
    sudo('cp /etc/httpd/conf.d/nagios.conf /etc/apache2/conf-available/nagios.conf')
    sudo('cp /etc/httpd/conf.d/nagios.conf /etc/apache2/conf-enabled/nagios.conf')
    sudo('rm -rf /etc/apache2/conf-available/nagios3.conf')
    sudo('rm -rf /etc/apache2/conf-enabled/nagios3.conf')

@task
def prepare_apache():
    '''
    Creates Nagios admin user and configures Apache.
    '''
    sudo(str('htpasswd -bc /usr/local/nagios/etc/htpasswd.users %s %s'% (nagios_server_user, nagios_server_password)))
    sudo('/etc/init.d/apache2 reload')

@task
def install_nagios_plugins_from_source():
    '''
    Downloads Nagios plugins source code and installs Nagios plugins on VM.
    '''
    if not nagios_plugins_downloaded():
        sudo('wget http://nagios-plugins.org/download/nagios-plugins-2.0.3.tar.gz')
    sudo('tar xzf nagios-plugins-2.0.3.tar.gz')
    sudo('cd ~/nagios-plugins-2.0.3 && ./configure --with-nagios-user=nagios --with-nagios-group=nagios && make && make install')

@task
def install_nrpe_plugin_from_source():
    '''
    Downloads NRPE plugin source code and installs NRPE plugin on VM.
    '''
    cuisine.package_ensure_apt('libssl-dev')
    cuisine.dir_ensure('/usr/local/src')
    run('cd /usr/local/src')
    if not nrpe_plugins_downloaded():
        sudo('wget http://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz')
    sudo('tar xzf nrpe-2.15.tar.gz')
    sudo('cd ~/nrpe-2.15 && ./configure --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu && make all && make install-plugin')

@task
def start_nagios():
    '''
    Starts Nagios on VM and sets up Nagios as upstart job.
    '''
    put('./commands.cfg','/usr/local/nagios/etc/objects/commands.cfg', use_sudo=True)
    sudo('ln -sf /etc/init.d/nagios /etc/rcS.d/S99nagios')
    sudo('/etc/init.d/nagios start')


execute(add_nagios_user)
execute(install_prerequisites)
execute(install_nagios_from_source)
execute(prepare_apache)
execute(install_nrpe_plugin_from_source)
execute(start_nagios)

