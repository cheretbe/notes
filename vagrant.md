* https://app.vagrantup.com

```
  config.winrm.password = "password"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "1024"
    vb.cpus = "1"
    vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    vb.customize ["sharedfolder", "add", :id, "--name", "provision", "--hostpath", "/path/on/host"]
  end
```

```shell
# List boxes
vagran box list

# List updates
vagrant box outdated --global
# Add latest version of a box
vagrant box add --clean centos/7 --provider virtualbox
# Remove all old versions
vagrant box prune

# View all know Vagrant VMs
vagrant global-status

# Add a box from a local file
vagrant box add my-box file://path/to/file.box
# Windows
vagrant box add my-box file:///d:/path/to/file.box
vagrant box add my-box file:////network/share/file.box
```

To move data from `%USERPROFILE%\.vagrant.d` `VAGRANT_HOME` environment variable needs to be set.
```shell
# Bash, set permanently
echo export VAGRANT_HOME=/path/to/home >> ~/.bashrc
```

### API

* https://www.vagrantup.com/docs/vagrant-cloud/api.html

```bash
# List all boxes for a user
curl "https://app.vagrantup.com/api/v1/user/username"
```

### Plugins
* hostmanager (name resolution when IP addresses are not known in advance): https://github.com/devopsgroup-io/vagrant-hostmanager
* https://github.com/emyl/vagrant-triggers

### Automatic plugins installation

```ruby
required_plugins = %w( vagrant-triggers )

plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
if not plugins_to_install.empty?
  puts "Installing plugins: #{plugins_to_install.join(' ')}"
  if system "vagrant plugin install #{plugins_to_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort "Installation of one or more plugins has failed. Aborting."
  end
end
```
```ruby
unless Vagrant.has_plugin?('vagrant-triggers')
  system('vagrant plugin install vagrant-triggers') || raise
  warn 'Restarting...'
  exec($0, *ARGV)
end
```

Notification only
```ruby
required_plugins = %w( vagrant-triggers vagrant-hostmanager)

plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }
if not plugins_to_install.empty?
  puts "This Vagrantfile needs one or more additional plugins to be installed: #{plugins_to_install.join(', ')}"
  puts "Use the following command:\n\n"
  puts "vagrant plugin install #{plugins_to_install.join(' ')}\n\n"
  abort "Installation of one or more additional plugins needed. Aborting."
end
```


### Packer

* VB+QEMU: https://github.com/pear2/Net_RouterOS/blob/master/tests/vm/RouterOS.packer.json
* https://github.com/dulin/vagrant-mikrotik
