# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 13:33:53 2014

@author: Konstantin
"""
import keystoneclient.v2_0.client as ksclient
from novaclient import client as noclient
import config_transporter, pickle


KEYSTONE_CONN = ksclient.Client(
    auth_url='http://lisa.cloudcomplab.ch:35357/v2.0',
    username='benn',
    password='icclab123',
    tenant='zhaw-users')

print(KEYSTONE_CONN.authenticate())

OS_TOKEN = KEYSTONE_CONN.get_token(KEYSTONE_CONN.session)


NOVA_CONN = noclient.Client('1.1',
                            auth_url='http://lisa.cloudcomplab.ch:35357/v2.0',
                            username='benn',
                            auth_token=OS_TOKEN,
                            tenant_id='36e520370bf742bba3f09690af98b46d')

print(NOVA_CONN.servers.list())

SERVERS = [(server.name,
            server.hostId,
            server.to_dict()['addresses'].values()[0][0]['addr'])
           for server in NOVA_CONN.servers.list('dict')
           if server.user_id == u'e87d5f264369457181bf9e374febc04b']
print(SERVERS)

NAGIOS_SERVER = NOVA_CONN.servers.find(name='nagios_test')

VM_LIST = [
    config_transporter.add_file_to_nagios_conf_dir(name=server[0],
                                                   ip=server[2])
    for server in SERVERS]

pickle.dump(SERVERS, open('server_list', 'w'))

config_transporter.write_intermediate_file()
