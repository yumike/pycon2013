# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.forward_port 80, 8080
  config.vm.share_folder "salt_file_root", "/srv", "salt/roots/"

  config.vm.provision :salt do |salt|
    salt.run_highstate = true
    salt.salt_install_type = "git"
    salt.salt_install_args = "v0.12.1"
  end
end
