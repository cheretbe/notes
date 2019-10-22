* https://app.vagrantup.com
* https://github.com/dotless-de/vagrant-vbguest/issues/298
* :warning: **https://dzone.com/articles/environment-variable-with-vagrant-and-ansible**

```ruby
# Manually setting box version
config.vm.box = "centos/7"
config.vm.box_version=1804.02
```

```shell
vagrant ssh-config > /tmp/ssh-config-name
scp -F /tmp/ssh-config-name default:filename .
```

```ruby

# Multi-machine with autostart disabled
Vagrant.configure("2") do |config|
  config.vm.define :host1, autostart: false do |host1|
    host1.vm.box = "ubuntu/xenial64"
    # etc
  end
end
  
  # SecondHDD = "/full/path/to/vm-name_second_hdd.vdi"
  SecondHDD = "./vm-name_second_hdd.vdi"
  
  # Disable the default /vagrant share
  config.vm.synced_folder ".", "/vagrant", disabled: true

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
    # deny|allow-vms|allow-all
    vb.customize [ "modifyvm", :id, "--nicpromisc2", "allow-all" ]
    
    unless File.exist?(SecondHDD)
      vb.customize ['createhd', '--filename', SecondHDD, '--variant', 'Standard', '--size', 20*1024]
    end
    # "SATAController", "--port", 1
    vb.customize ['storageattach', :id,  '--storagectl', 'SCSI', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', SecondHDD]
  end

  config.vm.network "private_network", virtualbox__intnet: "vagrant-intnet-1", auto_config: false
  config.vm.network "private_network", ip: "172.24.0.1", virtualbox__intnet: "vagrant-intnet-2"
  config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "vagrant-intnet-3"
  # [!] Host-only network
  config.vm.network "private_network", type: "dhcp", auto_config: false
  # Bridged adapter
  # https://www.vagrantup.com/docs/networking/public_network.html
  config.vm.network "public_network", ip: "192.168.1.17"
  
  # https://www.vagrantup.com/docs/provisioning/shell.html
  # [!!] Works with Powershell (additional options are available: powershell_elevated_interactive and powershell_args)
  config.vm.provision "shell", name: "test", keep_color: true, inline: "apt-get -y -q update && apt-get -y -q install git"
  config.vm.provision "shell", name: "Multi-line command test",
    keep_color: true, privileged: false,
    inline: <<-SHELL
      ls -lha /
      uname -a
    SHELL
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
### AWS
* https://github.com/mitchellh/vagrant-aws
```shell
echo $(cat .vagrant/machines/default/aws/id)
aws ec2 describe-instances \
--instance-id $(cat .vagrant/machines/default/aws/id) \
--query 'Reservations[0].Instances[0].PublicIpAddress'
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

      env.cli("ssh", "--", "hostname", "-f")
    end
  end
```
* https://github.com/hashicorp/vagrant/blob/master/website/source/docs/triggers/index.html.md
* https://github.com/hashicorp/vagrant/blob/master/website/source/docs/triggers/usage.html.md
* https://github.com/hashicorp/vagrant/blob/master/website/source/docs/triggers/configuration.html.md
* https://www.vagrantup.com/docs/plugins/development-basics.html
* https://www.vagrantup.com/docs/plugins/commands.html
* https://github.com/hashicorp/vagrant/blob/master/lib/vagrant/ui.rb
* https://github.com/hashicorp/vagrant/blob/master/lib/vagrant/environment.rb
* https://github.com/hashicorp/vagrant/blob/master/plugins/commands/up/command.rb
* https://www.rubydoc.info/github/mitchellh/vagrant/Vagrant/Environment
* https://stackoverflow.com/questions/21890104/run-code-in-vagrantfile-only-if-provisioning
* https://stackoverflow.com/questions/24855635/check-if-vagrant-provisioning-has-been-done/38203497#38203497

### Debugging
```shell
cp /opt/vagrant/embedded/gems/2.2.2/gems/vagrant-2.2.2/vagrant.gemspec{,.bak}
nano /opt/vagrant/embedded/gems/2.2.2/gems/vagrant-2.2.2/vagrant.gemspec

# Add these lines
s.add_dependency 'pry'
s.add_dependency 'pry-byebug'

/opt/vagrant/embedded/bin/gem install pry pry-byebug --install-dir /opt/vagrant/embedded/gems/2.2.2

# In Vagrant file
# require "pry"
# binding.pry

```

### API

* https://www.vagrantup.com/docs/vagrant-cloud/api.html

```bash
# List all boxes for a user
curl "https://app.vagrantup.com/api/v1/user/username"
```

### Plugins
* https://github.com/dotless-de/vagrant-vbguest#global-configuration
     * https://github.com/dotless-de/vagrant-vbguest/issues/226
     * https://github.com/dotless-de/vagrant-vbguest#global-configuration
     * `~/.vagrant.d/Vagrantfile`:
```ruby
Vagrant.configure("2") do |config|
  config.vbguest.auto_update = false
end
```
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
* https://github.com/dotless-de/vagrant-vbguest#global-configuration

### Environment variables transfer
```ruby
env_vars = ["VAR1", "VAR2"]

# This code is executed on every Vagrant command, therefore, we don't check
# anything and don't echo any messages here. All necessary checks should be
# done in the provision script
env_vars_with_values = Hash.new
env_vars.each do |env_var|
  env_vars_with_values[env_var] = ENV[env_var]
end

# ...
  config.vm.provision "shell", path: "../../provision/env_vars.sh", keep_color: true,
    env: env_vars_with_values, args: [env_vars.join(" ")], privileged: false
```
```shell
#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

grep -qxF 'source ~/custom_env_vars.sh' ~/.profile || printf "\nsource ~/custom_env_vars.sh\n" >> ~/.profile

echo "Setting custom environment variables"
echo "# Custom environment variables" > ~/custom_env_vars.sh
chmod 600 ~/custom_env_vars.sh
for env_var in ${1}; do
  echo "  ${env_var}"
  if [ -z "${!env_var}" ]; then
    >&2 echo "Environment variable '${env_var}' is not defined"
    >&2 echo "For this Vagrantfile to work correctly the following " \
      "environment variables need to be defined: ${1}"
    exit 1
  fi
  echo "export ${env_var}=${!env_var}" >>~/custom_env_vars.sh
done

exit 0
```
Use with non-interactive shell
```shell
vagrant ssh -- bash -lc export
```

### Packer

* VB+QEMU: https://github.com/pear2/Net_RouterOS/blob/master/tests/vm/RouterOS.packer.json
* https://github.com/dulin/vagrant-mikrotik
