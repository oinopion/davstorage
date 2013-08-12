# -*- mode: ruby -*-
# vi: set ft=ruby :

# Run 'vagrant up' to start server
# Apache will be available at localhost:6000
# Nginx will be available at localhost:7000
# Both share htpass and data directory
# To upload file via PUT do:
# $ curl 'http://vagrant:vagrant@localhost:7000/hello.txt' -T hello.txt
# To create collection do:
# $ curl 'http://vagrant:vagrant@localhost:7000/images' -X MKCOL
# To access file:
# curl 'http://localhost:7000/hello.txt'

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :forwarded_port, guest: 80, host: 9000
  config.vm.network :forwarded_port, guest: 8000, host: 7000
  config.vm.provision :shell, path: "provision.sh"
end
