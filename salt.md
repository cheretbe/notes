* **https://www.linode.com/docs/applications/configuration-management/beginners-guide-to-salt/**
* https://medium.com/@Joachim8675309/vagrant-provisioning-with-saltstack-50dab12ce6c7
* https://github.com/hbokh/awesome-saltstack
* https://medium.com/@timlwhite/the-simplest-way-to-learn-saltstack-cd9f5edbc967
* https://github.com/aldevar/Zabbix_SaltState/blob/master/init.sls
* http://nghenglim.github.io/saltstack-vagrant-part-1/
* https://www.tutorialspoint.com/saltstack/saltstack_quick_guide.htm
* https://bencane.com/2016/03/22/self-managing-servers-with-masterless-saltstack-minions/
* https://www.linode.com/docs/applications/configuration-management/automate-a-static-site-deployment-with-salt/
* https://github.com/saltstack/salt-bootstrap#install-using-curl

Masterless

```shell
wget -O - https://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
echo "deb http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest bionic main" >/etc/apt/sources.list.d/saltstack.list
apt update
apt install salt-minion
```
/etc/salt/minion.d/masterless.conf


* https://docs.saltstack.com/en/latest/topics/tutorials/states_pt3.html
* https://github.com/harkx/saltstack-cheatsheet#grains
```
salt-call --local grains.ls
salt-call --local grains.item os
```
