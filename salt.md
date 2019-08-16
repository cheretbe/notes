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

Masterless

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
