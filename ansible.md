* https://www.redhat.com/en/blog/system-administrators-guide-getting-started-ansible-fast
* http://codeheaven.io/15-things-you-should-know-about-ansible/
* https://github.com/ansible/awx
* https://docs.ansible.com/ansible-tower/latest/html/quickstart/launch.html
* **https://averytechguy.com/2019/01/19/auto-remediation-with-zabbix-and-ansible-tower-part-2/**
* https://www.unixarena.com/2019/03/ansible-tower-awx-creating-workflow-template.html/
* https://medium.com/@ripon.banik/getting-started-with-ansible-tower-awx-part2-74ad8e380d34
* https://pypi.org/project/ansible-tower-cli/
* **https://www.redhat.com/en/blog/adding-remediation-zabbix-using-ansible-tower**
* **https://docs.ansible.com/ansible-tower/latest/html/administration/tipsandtricks.html**
* https://github.com/debops/debops-tools/issues/120
---------
* https://stackoverflow.com/questions/41535838/how-to-run-apt-update-and-upgrade-via-ansible-shell/41537418#41537418
* https://github.com/crazed014/bootstrap-awx/blob/master/deploy_awx_ubuntu1804.sh
* https://www.reddit.com/r/ansible/comments/9r2gwh/awx_stuck_in_awx_upgrading_phase/
* https://stackoverflow.com/questions/25230376/how-to-automatically-install-ansible-galaxy-roles
---------
* https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
* http://www.juliosblog.com/ansible-and-ansible-tower-best-practices-from-the-field/
* :question: https://github.com/enginyoyen/ansible-best-practises
    * Do not manage external roles in your repository manually, use ansible-galaxy
* https://blog.theodo.com/2015/10/best-practices-to-build-great-ansible-playbooks/
    * Put the community’s roles in a separate folder
    * Explore Ansible Galaxy. There are many great roles over there. Instead of rewriting everything go forking! 
* http://www.markusz.io/posts/2017/11/24/ansible-playbook-roles/
* https://opencredo.com/blogs/reusing-ansible-roles-with-private-git-repos-and-dependencies/
* https://openedx.atlassian.net/wiki/spaces/OpenOPS/pages/26837527/Ansible+Code+Conventions


`export ANSIBLE_HOST_KEY_CHECKING=False` while you're deploying new servers, then remove it with `unset ANSIBLE_HOST_KEY_CHECKING`.

### AWX
Installation
```
apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg-agent \
     software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
     
apt-get update
apt-get install docker-ce

apt-get install python-pip
pip install docker docker-compose

apt install nodejs npm -y
npm install npm --global

# https://github.com/ansible/awx/blob/devel/INSTALL.md
git clone --depth 1 https://github.com/ansible/awx

cd awx/installer/
sed -i 's+ansible_python_interpreter="/usr/bin/env python"+ansible_python_interpreter="/usr/bin/env python3"+' inventory
sed -i 's+docker_compose_dir=/tmp/awxcompose+docker_compose_dir=/opt/awx/awxcompose+' inventory
sed -i 's+postgres_data_dir=/tmp/pgdocker+postgres_data_dir=/opt/awx/pgdocker+' inventory
cat inventory | grep -v "#" |sort -n | grep .
ansible-playbook -i inventory install.yml
# Wait for migration to complete
docker logs -f awx_task
```
Tower CLI
```shell
pip3 install ansible-tower-cli
tower-cli config host http://localhost:80
tower-cli config verify_ssl false
tower-cli config username admin
tower-cli config password password

# View current config
tower-cli config

# Backup AWS config
tower-cli receive --all > backup.json
# Restore config from the backup
tower-cli send backup.json
```
* http://elatov.github.io/2018/12/setting-up-and-using-awx-with-docker-compose/
* https://github.com/geerlingguy/ansible-vagrant-examples/issues/48
* Credentials backup/restore: https://github.com/ansible/tower-cli/issues/529
