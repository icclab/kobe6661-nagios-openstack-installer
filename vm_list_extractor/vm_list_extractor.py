# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 13:33:53 2014

@author: Konstantin
"""
import keystoneclient.v2_0.client as ksclient
from novaclient import client as noclient
import pickle, configparser

config = configparser.ConfigParser()
config.read('/usr/local/nagios/config.ini')
print(config.sections())

openstack_credentials = dict(config['OPENSTACK_CREDENTIALS'])
os_username = str(openstack_credentials['os.username'])
os_password = str(openstack_credentials['os.password'])
os_tenant = str(openstack_credentials['os.tenant'])
os_auth_url = str(openstack_credentials['os.auth_url'])

KEYSTONE_CONN = ksclient.Client(
    auth_url=os_auth_url,
    username=os_username,
    password=os_password,
    tenant=os_tenant)

print(KEYSTONE_CONN.authenticate())

OS_TOKEN = KEYSTONE_CONN.get_token(KEYSTONE_CONN.session)
RAW_TOKEN = KEYSTONE_CONN.get_raw_token_from_identity_service(
    auth_url=os_auth_url,
    username=os_username,
    password=os_password,
    tenant_name=os_tenant)

os_user_id = KEYSTONE_CONN.auth_user_id
os_tenant_id = RAW_TOKEN['token']['tenant']['id']


NOVA_CONN = noclient.Client('1.1',
                            auth_url=os_auth_url,
                            username=os_username,
                            auth_token=OS_TOKEN,
                            tenant_id=os_tenant_id)

print(NOVA_CONN.servers.list())

SERVERS = [(server.name,
            server.hostId,
            server.to_dict()['addresses'].values()[0][0]['addr'])
           for server in NOVA_CONN.servers.list('dict')
           if server.user_id == os_user_id]
print(SERVERS)

NAGIOS_SERVER = NOVA_CONN.servers.find(name='nagios_test')

#VM_LIST = [
#    config_transporter.add_file_to_nagios_conf_dir(name=server[0],
#                                                   ip=server[2])
#    for server in SERVERS]

pickle.dump(SERVERS, open('/usr/local/nagios/etc/server_list', 'w'))
