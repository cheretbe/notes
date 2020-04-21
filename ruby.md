* https://rvm.io/rvm/install

Ubuntu
```
apt-get install software-properties-common
apt-add-repository -y ppa:rael-gc/rvm
apt-get update
apt-get install rvm
# also as root
. /etc/profile.d/rvm.sh
rvm install ruby

# back as regular user run this or re-login
. /etc/profile.d/rvm.sh

# Run interactive Ruby shell
irb
```
