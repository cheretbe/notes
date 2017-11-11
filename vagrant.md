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

### Plugins
* hostmanager (name resolution when IP addresses are not known in advance): https://github.com/devopsgroup-io/vagrant-hostmanager
