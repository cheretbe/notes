* :point_right: https://docs.saltproject.io/en/getstarted/overview.html
* :bulb: https://salt.tips/text-editor-plugins-for-salt-states-and-yaml-jinja/#visual-studio-code
    * VSCode extension for SaltStack is available on the Marketplace. To install it click `File` -> `Preferences` -> `Extensions`, then search for saltstack and click install. The source code is available on [GitHub](https://github.com/korekontrol/vscode-saltstack)
* **https://www.linode.com/docs/applications/configuration-management/beginners-guide-to-salt/**
* **https://serverfault.com/questions/590755/hostname-of-minion-in-salt-command/615852#615852**
* https://www.linode.com/docs/applications/configuration-management/introduction-to-jinja-templates-for-salt/
* https://www.linode.com/docs/applications/configuration-management/introduction-to-jinja-templates-for-salt/#salt-and-jinja-best-practices
* **https://implement.pt/2018/10/a-comprehensive-introduction-to-salt/**
* **https://www.reddit.com/r/saltstack/comments/4hfe2q/use_saltstack_to_update_linux_hosts/d2qx7pa?utm_source=share&utm_medium=web2x**
* https://medium.com/@Joachim8675309/vagrant-provisioning-with-saltstack-50dab12ce6c7
* https://github.com/hbokh/awesome-saltstack
* https://medium.com/@timlwhite/the-simplest-way-to-learn-saltstack-cd9f5edbc967
* https://github.com/aldevar/Zabbix_SaltState/blob/master/init.sls
* http://nghenglim.github.io/saltstack-vagrant-part-1/
* https://www.tutorialspoint.com/saltstack/saltstack_quick_guide.htm
* https://bencane.com/2016/03/22/self-managing-servers-with-masterless-saltstack-minions/
* https://www.linode.com/docs/applications/configuration-management/automate-a-static-site-deployment-with-salt/
* https://github.com/saltstack/salt-bootstrap#install-using-curl
* https://stackoverflow.com/questions/52746217/call-a-salt-state-from-another-salt-state/52756463#52756463

### General info

* **Salt Master** - Central management system
* **Salt Minions** - Managed systems
* **Execution Modules** - Ad hoc commands executed from the command line against one or more managed systems
* **Formulas (States)** - A declarative or imperative representation of a system configuration
* **Grains** - System variables. Grains are static information about the underlying managed system and include operating system, memory, and many other system properties. You can also define custom grains for any system.
* **Pillars** - User-defined variables. These secure variables are defined and stored on the Salt Master and then "assigned" to one or more minions using targets.
* **Top File** - Matches formulas and Salt pillar data to Salt minions


`/etc/salt/master.d/gitfs.conf` example?

```shell
salt-key -L | less
salt-key --accept host.domain.tld
salt host.domain.tld saltutil.running
salt host.domain.tld cmd.run "hostname -f; uptime"

salt-run manage.up
salt-run manage.status
salt-run manage.down
salt-run manage.versions
# Gives a full list of all the modules you can run with salt-run
salt-run -d
```

### Master

:warning: 2check:
```
/usr/lib/python2.7/dist-packages/salt/scripts.py:198: DeprecationWarning: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date.  Salt will drop support for Python 2.7 in the Sodium release or later.
```

```shell
wget -O - https://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo "deb http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest bionic main" | sudo tee /etc/apt/sources.list.d/saltstack.list
sudo apt update
# 2check: do we need salt-cloud and salt-syndic?
sudo apt -y install salt-api salt-cloud salt-master salt-minion salt-ssh salt-syndic

# Config is in /etc/salt/master
# Default config is OK

cp /etc/salt/minion{,.bak}
nano /etc/salt/minion
# Change master to
# master: localhost
systemctl restart salt-minion

salt-key -L
salt-key --accept=saltstack.domain.tld
# or just
salt-key -A
```

Git repo backend.
* https://www.linode.com/docs/applications/configuration-management/automate-a-static-site-deployment-with-salt/
```shell
apt install python-pygit2

```

Edit `/etc/salt/master`:
```
fileserver_backend:
  - roots
  - git

gitfs_remotes:
  - https://github.com/cheretbe/saltstack-formulas.git
```
```shell
# Apply changes
service salt-master restart

# Default update interval is 60 seconds
# https://docs.saltstack.com/en/latest/ref/configuration/master.html#std:conf_master-gitfs_update_interval
# Manually fetch git repo
sudo salt-run fileserver.update

```

### Masterless

```shell
wget -O - https://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo "deb http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest bionic main" >/etc/apt/sources.list.d/saltstack.list
apt update
apt install salt-minion

# This does the same
wget https://raw.githubusercontent.com/saltstack/salt-bootstrap/stable/bootstrap-salt.sh
bash bootstrap-salt.sh stable

salt-minion --version
service salt-minion stop
```
/etc/salt/minion.d/masterless.conf
```
file_client: local
```

```shell
salt-call --local state.highstate -l debug
```


* https://docs.saltstack.com/en/latest/topics/tutorials/states_pt3.html
* https://github.com/harkx/saltstack-cheatsheet#grains
```
salt-call --local -g
salt-call --local grains.ls
salt-call --local grains.item os
```
