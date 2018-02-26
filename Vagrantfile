# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "pddev" do |dev|
    dev.vm.box = "ubuntu/xenial64"
    dev.vm.host_name = "pddev"
    dev.vm.network :private_network, ip: "10.1.0.2"
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "512"]
        vb.customize ["modifyvm", :id, "--ioapic", "on"]
        vb.customize ["modifyvm", :id, "--cpus", "2"]
        vb.linked_clone = true
    config.vm.synced_folder ".", "/vagrant",
        type: "virtualbox",
        mount_options: ["dmode=775,fmode=775"]
    end
    config.vm.provision "shell", path: "Vagrant_bootstrap.sh"
  end

end
