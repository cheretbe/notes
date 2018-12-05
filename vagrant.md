* https://app.vagrantup.com

```shell
vagrant ssh-config > /tmp/ssh-config-name
scp -F /tmp/ssh-config-name default:filename .
```

```ruby
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.winrm.password = "password"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "1024"
    vb.cpus = "1"
    vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    # absolute path
    vb.customize ["sharedfolder", "add", :id, "--name", "provision", "--hostpath", "/path/on/host", "--automount"]
    # relative path
    vb.customize ["sharedfolder", "add", :id, "--name", "debug", "--hostpath", File.expand_path("../..", File.dirname(__FILE__)), "--automount"]
  end
  config.vm.network "private_network", virtualbox__intnet: "vagrant-intnet-1", auto_config: false
  config.vm.network "private_network", ip: "172.24.0.1", virtualbox__intnet: "vagrant-intnet-2"
  config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "vagrant-intnet-3"
  # [!] Host-only network
  config.vm.network "private_network", type: "dhcp", auto_config: false
```

```shell
# List boxes
vagran box list

# Add latest version of a box
# --clean Clean any temporary download files
vagrant box add --clean centos/7 --provider virtualbox

# List updates
vagrant box outdated --global

# Update a specific box (not tied to a Vagrant environment) 
vagrant box update --box centos/7

# Remove all old versions
vagrant box prune

# View all know Vagrant VMs
vagrant global-status

# Add a box from a local file
vagrant box add my-box file://path/to/file.box
# Windows
vagrant box add my-box file:///d:/path/to/file.box
vagrant box add my-box file:////network/share/file.box

# Create a box from a Virtualbox VM
vagrant package --base my_test --output my_test.box --vagrantfile vagrantfile-my_test.template
```

To move data from `%USERPROFILE%\.vagrant.d` `VAGRANT_HOME` environment variable needs to be set.
```shell
# Bash, set permanently
echo export VAGRANT_HOME=/path/to/home >> ~/.bashrc
```

### Triggers
```ruby
  config.trigger.after :provision do |trigger|
    trigger.info = "provision test"
    trigger.ruby do |env,machine|
      #puts env.to_yaml
      #File.open("output.yml", "w") { |file| file.write(env.to_yaml) }
      #puts machine.ssh_info

      #puts ARGV.to_yaml
      #ARGV.each do |arg|
      #  puts (" argument: " + arg)
      #end

      env.ui.say(:error, "error test")
      env.ui.say(:detail, "detail test")
      env.ui.say(:info, "info test")
      env.ui.say(:success, "success test")
    end
  end
```

* https://www.vagrantup.com/docs/plugins/development-basics.html
* https://github.com/hashicorp/vagrant/blob/master/lib/vagrant/ui.rb

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
