```shell
# List boxes
vagran box list

# List updates
vagrant box outdated --global
# Add latest version of a box
vagrant box add --clean centos/7 --provider virtualbox
# Remove all old versions
vagrant box prune -f
```
