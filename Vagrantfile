require 'vagrant-openstack-provider'

Vagrant.configure('2') do |config|

  config.vm.box       = 'openstack'
  config.ssh.username = 'stack'

  config.vm.provider :openstack do |os|
    os.openstack_auth_url = 'http://lisa.cloudcomplab.ch:35357/v2.0'
    os.username           = 'benn'
    os.password           = 'icclab123'
    os.tenant_name        = 'zhaw-users'
    os.flavor             = 'm1.small'
    os.image              = 'ubuntu-14-04-server-cloudinit'
    os.floating_ip_pool   = 'net04_ext'
  end
end