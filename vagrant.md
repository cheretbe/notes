
* https://app.vagrantup.com
* https://github.com/dotless-de/vagrant-vbguest/issues/298
* :warning: **https://dzone.com/articles/environment-variable-with-vagrant-and-ansible**
* Reboot during provision: https://github.com/dotless-de/vagrant-vbguest/blob/main/lib/vagrant-vbguest/installers/centos.rb#L100

----
* Additional HDD
    * https://developer.hashicorp.com/vagrant/docs/disks/configuration
    * https://www.lukmanlab.com/how-to-add-new-disk-in-vagrant/
      ```
      config.vm.disk :disk, size: "10GB", name: "zfs_disk_1"
      config.vm.disk :disk, size: "10GB", name: "zfs_disk_2"
      config.vm.disk :disk, size: "8GB",  name: "zfs_disk_3"
      ```

```shell
# libvirt
sudo apt install libvirt-dev build-essential
vagrant plugin install vagrant-libvirt
vagrant up --provider=libvirt
# or set env variable
export VAGRANT_DEFAULT_PROVIDER=libvirt
# https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html
# https://github.com/vagrant-libvirt/vagrant-libvirt/blob/main/lib/vagrant-libvirt/action/create_network_interfaces.rb

# Installation on Ubuntu 22.04
wget https://apt.releases.hashicorp.com/gpg -O /usr/share/keyrings/hashicorp.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp.asc] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list
apt update
sudo apt install vagrant
```

```
vboxmanage controlvm $(cat .vagrant/machines/default/virtualbox/id) \
  natpf1 "forward_port_80,tcp,,8080,,80"
  
vboxmanage showvminfo $(cat .vagrant/machines/default/virtualbox/id) --machinereadable | grep Forwarding

route add default gw 192.168.0.1 metric 10
route delete default gw 192.168.0.1 metric 10

export GW_ADDR=192.168.0.1
# Fastly (apt.releases.hashicorp.com)
route add -net 151.101.0.0/16 gw $GW_ADDR metric 10
# Amazon-4 (vagrantcloud.com)
route add -net 52.84.0.0/15 gw $GW_ADDR metric 10
```

`.gitignore` contents:
```
/.vagrant/
```

```ruby
# Fix console log file creation issue for Ubuntu boxes
vbox_version = Gem::Version.new(VagrantPlugins::ProviderVirtualBox::Driver::Meta.new.version)

if vbox_version < Gem::Version.new("6.0") then
  # vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
  vb.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
end

# Also test this
vb.customize ["modifyvm", :id, "--uart1", "off"]
vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
```

```ruby
# Manually setting box version
config.vm.box = "centos/7"
config.vm.box_version=1804.02
```
`/etc/fstab` example:
```
share_name  /path/to/mountpoint  vboxsf  rw,exec,uid=vagrant,gid=vboxsf,dmode=775,fmode=664  0   0
```

```shell
vagrant ssh-config > /tmp/ssh-config-name
scp -F /tmp/ssh-config-name default:filename .

echo $(cat .vagrant/machines/default/virtualbox/id)
# For multi-machine Vagrantfile
echo $(cat .vagrant/machines/machine-name/virtualbox/id)
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
    # NICs are 1-based (--nicpromisc<1-N>, --nictype<1-N>, etc.)
    # deny|allow-vms|allow-all
    vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    # Virtio supports VLAN tagging in guests
    # [!] NICs are 1-based
    vb.customize ["modifyvm", :id, "--nictype2", "virtio"]

    
    unless File.exist?(SecondHDD)
      vb.customize ['createhd', '--filename', SecondHDD, '--variant', 'Standard', '--size', 20*1024]
    end
    # "SATAController", "--port", 1
    vb.customize ['storageattach', :id,  '--storagectl', 'SCSI', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', SecondHDD]
  end

  # https://www.vagrantup.com/docs/provisioning/shell.html
  # [!!] Works with Powershell (additional options are available: powershell_elevated_interactive and powershell_args)
  config.vm.provision "shell", name: "test", keep_color: true, inline: "apt-get -y -q update && apt-get -y -q install git"
  config.vm.provision "shell", name: "Multi-line command test",
    keep_color: true, privileged: false,
    inline: <<-SHELL
      ls -lha /
      uname -a
      # note a double backslash here
      ls /dir1 && \\
      ls /dir2
    SHELL
```
##### Port forwarding

* https://github.com/hashicorp/vagrant/blob/main/website/content/docs/networking/forwarded_ports.mdx
* https://github.com/hashicorp/vagrant/blob/main/plugins/providers/virtualbox/model/forwarded_port.rb#L55
``` ruby
config.vm.network "forwarded_port",
  # bind ssh to all interfaces instead of default 127.0.0.1 ([!] security implications)
  guest: 22, host: 2222, host_ip: "0.0.0.0", id: "ssh", auto_correct: true
```


For privileged ports (most likely not needed at all):
```
vagrant ssh-config > /tmp/ssh-config-name
# -g      Allows remote hosts to connect to local forwarded ports.  If used on a multiplexed connection, then this option must be specified on the master
             process.
sudo ssh -f /tmp/ssh-config-name -p 2222 -gNfL 80:localhost:80
# More advanced options is to run in the background with setting up a socket to be able to close the connection
# (not needed for simple vagrant tests)
# https://mpharrigan.com/2016/05/17/background-ssh.html
```
##### Networking
* https://www.vagrantup.com/docs/networking/private_network
* https://www.vagrantup.com/docs/networking/public_network.html
* https://www.vagrantup.com/docs/providers/virtualbox/networking
```ruby
# https://github.com/hashicorp/vagrant/blob/main/plugins/providers/virtualbox/action/network.rb
# hostonly_config
# auto_config: true, mac: nil, nic_type: nil, type: :static
# 
# intnet_config
# type: "static", ip: nil, netmask: "255.255.255.0", adapter: nil, mac: nil, intnet: nil, auto_config: true
#
# bridged_config
# auto_config: true, bridge: nil, mac: nil, nic_type: nil, use_dhcp_assigned_default_route: false
# nic_type options: Am79C970A|Am79C973|Am79C960|82540EM|82543GC|82545EM|virtio

config.vm.network "private_network", virtualbox__intnet: "vagrant-intnet-1", auto_config: false
config.vm.network "private_network", ip: "172.24.0.1", virtualbox__intnet: "vagrant-intnet-2"
config.vm.network "private_network", type: "dhcp", virtualbox__intnet: "vagrant-intnet-3"

# Host-only network
config.vm.network "private_network", type: "dhcp", auto_config: false

# Bridged adapter
config.vm.network "public_network", ip: "192.168.1.17"
# Virtualbox perfix is 08:00:27
# https://miniwebtool.com/mac-address-generator/
config.vm.network "public_network", bridge: "enp0s31f6", mac: "0800275A78D2", type: "dhcp"
```

##### Ansible provision
```ruby
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "ansible/provision.yml"
    ansible.compatibility_mode = "2.0"
    ansible.extra_vars = {
      "ansible_python_interpreter": "/usr/bin/python3",
      # then use in a playbook like that
      # when: my_env_var != None
      "my_env_var": ENV["MY_ENV_VAR"] || nil
    }
  end
```
```yaml
---

- name: Zabbix server provision
  hosts: all
  become: yes

  tasks:
    - name: Checkout shared playbooks repo
      git:
        repo: "https://github.com/cheretbe/ansible-playbooks.git"
        dest: "/ansible-playbooks"

    - include_role: name="/ansible-playbooks/zabbix-repo"
    - include_role: name="/ansible-playbooks/zabbix-server"

    - name: Install 'python3-pip' package
      apt:
        name: "python3-pip"
        # Fix for warning message "Could not find aptitude. Using apt-get instead"
        force_apt_get: yes
        update_cache: no

    - name: Install Python 3 'zabbix_api' package
      pip:
        name: zabbix_api
        executable: pip3
```

Command examples
```shell
# List boxes
vagrant box list

# Add latest version of a box
# --clean Clean any temporary download files
vagrant box add --clean centos/7 --provider virtualbox

# List updates
vagrant box outdated --global

# Update a specific box (not tied to a Vagrant environment) 
vagrant box update --box centos/7

# Remove all old versions
vagrant box prune

# Manually download box file
# alpine-linux/alpine-x86_64
# Get latest version
curl -s https://app.vagrantup.com/api/v1/box/alpine-linux/alpine-x86_64 | jq ".current_version.version"
# Assuming that latest version is "3.12.0"
wget https://app.vagrantup.com/alpine-linux/boxes/alpine-x86_64/versions/3.12.0/providers/virtualbox.box

# View all known Vagrant VMs
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

      # will not return control back
      env.cli("ssh", "--", "hostname", "-f")
    end
  end

# For now trigger types is an experimental feature. Activate it by
# setting VAGRANT_EXPERIMENTAL variable to 1
# VAGRANT_EXPERIMENTAL="1" vagrant up --provision
 
  config.trigger.after :"Vagrant::Action::Builtin::Provision", type: "action" do |trigger|
    trigger.ruby do |env,machine|
      # this fires too early when there is no network configured
      machine.ui.warn("after Vagrant::Action::Builtin::Provision")
    end
  end
  
  config.vm.provision "shell", inline: "uname -a"

  config.trigger.after :provisioner_run, type: "hook" do |trigger|
    trigger.ruby do |env,machine|
      # this needs some other provisioner configured (with no provisioners it isn't triggered)
      machine.ui.warn("after provisioner_run")
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
# VAGRANT_LOG env variable controls level of verbosity
# --debug options sets VAGRANT_LOG to debug, so the following two commands are equivalent
VAGRANT_LOG=debug vagrant status
vagrant --debug status
# [!!] debug level is way too verbose, try info level for a start
VAGRANT_LOG=info vagrant status
```

```shell
cp -a /opt/vagrant/embedded/gems/2.2.2{,.bak}

nano /opt/vagrant/embedded/gems/2.2.2/gems/vagrant-2.2.2/vagrant.gemspec

# Add these lines
s.add_dependency 'pry'
s.add_dependency 'pry-byebug'

/opt/vagrant/embedded/bin/gem install pry pry-byebug --install-dir /opt/vagrant/embedded/gems/2.2.2
```
```ruby
# In Vagrant file
require "pry"

# Add breakpoint
# in Vagrant file or in some module e.g. /opt/vagrant/embedded/gems/2.2.2/gems/vagrant-2.2.2/lib/vagrant/util/ssh.rb
# or /opt/vagrant/embedded/gems/2.2.2/gems/vagrant-2.2.2/plugins/commands/ssh/command.rb
binding.pry
```
Using pry
```
# To view variable's value just type its name
my_var
# List methods
ls my_var

next -- execute next line
step -- step into next function call
continue -- continue through stack
```
* https://gist.github.com/lfender6445/9919357

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
```ruby
  # CentOS 7 and 8
  config.vbguest.auto_update = true
  config.vbguest.installer_options = { allow_kernel_upgrade: true }
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

### Plugin develpment
* https://www.vagrantup.com/docs/plugins/
* https://github.com/hashicorp/vagrant/tree/master/website/source/docs/plugins
* https://github.com/hashicorp/vagrant/blob/master/lib/vagrant/plugin/v2/provisioner.rb
* https://www.vagrantup.com/docs/plugins/guest-capabilities.html
* https://github.com/mogproject/mog-infra/blob/master/docker-host/Vagrantfile
* https://blog.eduonix.com/system-programming/learn-implement-custom-provisioner/

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

Notes: [packer.md](./packer.md)
