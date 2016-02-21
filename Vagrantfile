Vagrant.require_version ">= 1.7.0"

Vagrant.configure(2) do |config|
  # config.vm.box = "opensuse-13.2"
  # config.vm.box_url = "https://susestudio.com/a/nCatAM/opensuse-13-2-for-vagrant"
  config.vm.box = "ubuntu/precise64"

  ########################################
  ### Saltstack master
  ########################################
  config.vm.define :saltmaster do |config|
    config.vm.hostname = "saltmaster.dev.darioblanco.com"
    config.vm.network :private_network, ip: "192.168.100.2"
    config.vm.synced_folder "roots/", "/srv/"

    config.vm.provider :virtualbox do |v|
      v.name = "saltmaster"
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--cpus", 1]
    end

    config.vm.provision :salt do |salt|
      salt.install_master = true
      salt.no_minion = true
      salt.seed_master = {
        "webserver.dev.darioblanco.com": "key/minion.pub"
      }  # Pre-seed the master
      salt.master_config = "master"
      salt.master_key = "key/master.pem"
      salt.master_pub = "key/master.pub"
    end
  end

  ########################################
  ### Nginx webserver example (Saltstack minion)
  ########################################
  config.vm.define :webserver do |config|
    config.vm.hostname = "webserver.dev.darioblanco.com"
    config.vm.network :private_network, ip: "192.168.100.3"

    config.vm.provider :virtualbox do |v|
      v.name = "webserver"
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--cpus", 1]
    end

    config.vm.provision :salt do |salt|
      salt.run_highstate = true  # Provision the machine
      salt.minion_config = "minion"
      salt.minion_id = "webserver"
      salt.minion_key = "key/minion.pem"
      salt.minion_pub = "key/minion.pub"
    end
  end

end
