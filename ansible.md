* Review when time permits: https://github.com/ekultails/rootpages/blob/master/src/automation/ansible.rst
------
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

### Roles and playbooks

* https://galaxy.ansible.com/docs/finding/content_types.html#ansible-roles
* https://linuxacademy.com/blog/linux-academy/ansible-roles-explained/
* https://docs.ansible.com/ansible/latest/modules/blockinfile_module.html#examples
* https://docs.ansible.com/ansible/latest/user_guide/playbooks_blocks.html
* 15 Things You Should Know About Ansible: https://habr.com/ru/post/306998/
* **https://molecule.readthedocs.io/en/stable/**
```yaml
# Useful host variables

# Allows to connect using IP instead of host's name
ansible_host: 10.10.10.10
```

```yaml
- name: populate service facts
  service_facts:

- debug:
    var: ansible_facts.services

  when: some_fact_that_contains_a_string|bool
  when: ansible_distribution_version|version_compare('15.04', '>=')
  
- name: Assertion
  assert:
    that:
      - result.images | length == 2
      
- name: Cancel
  fail:
    msg: "Debug"
```

### Installation

* https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-releases-via-apt-ubuntu
```
apt update
apt install software-properties-common
apt-add-repository --yes --update ppa:ansible/ansible
apt install ansible
```
`/etc/ansible/ansible.cfg`
```
[defaults]
# https://docs.ansible.com/ansible/2.8/reference_appendices/interpreter_discovery.html
interpreter_python = auto
```

### Windows

* https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#inventory-options
* https://docs.ansible.com/ansible-tower/latest/html/administration/kerberos_auth.html

### AWX
* https://github.com/ansible/awx
* https://www.unixarena.com/2018/10/ansible-how-to-install-and-configure-awx.html/
* https://www.unixarena.com/2018/11/ansible-tower-awx-organization-team-users-hierarchy.html/

Upgrade

According to [this FAQ](https://www.ansible.com/products/awx-project/faq) direct in-place upgrade isn't possible (See "Q: CAN I UPGRADE FROM ONE VERSION OF AWX TO ANOTHER?). But it looks like in latest versions the upgrade does work. At least 6.1.0 -> 7.0.0 migration went fine.
```shell
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images | grep awx | awk '{ print $3 }')
# Then run installer/install.yml from a new version using /opt/awx/inventory
# Rewview default inventory changes before installation
diff awx-6.1.0/installer/inventory awx-7.0.0/installer/inventory
```

Installation
```shell
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

apt-get install python3-pip
pip3 install docker docker-compose

apt install nodejs npm -y
npm install npm --global

# https://github.com/ansible/awx/blob/devel/INSTALL.md
#git clone --depth 1 https://github.com/ansible/awx
#cd awx/installer/

# The repo doesn't use Github release API, so this fails
# awx_ver=$(curl -s https://api.github.com/repos/ansible/awx/releases/latest | jq -r '.tarball_url')

wget https://github.com/ansible/awx/archive/7.0.0.tar.gz
tar xzvf 7.0.0.tar.gz
mkdir -p /opt/awx
cp awx-7.0.0/installer/inventory /opt/awx/

sed -i 's+ansible_python_interpreter="/usr/bin/env python"+ansible_python_interpreter="/usr/bin/env python3"+' /opt/awx/inventory
sed -i 's+docker_compose_dir=/tmp/awxcompose+docker_compose_dir=/opt/awx/awxcompose+' /opt/awx/inventory
sed -i 's+postgres_data_dir=/tmp/pgdocker+postgres_data_dir=/opt/awx/pgdocker+' /opt/awx/inventory
cat /opt/awx/inventory | grep -v "#" |sort -n | grep .
ansible-playbook -i /opt/awx/inventory awx-7.0.0/installer/install.yml
# Wait for migration to complete
docker logs -f awx_task

docker exec -ti awx_task /bin/bash
```

Uninstallation
```shell
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images | grep awx | awk '{ print $3 }')
rm -rf /opt/awx/awxcompose
rm -rf /opt/awx/pgdocker
```

Tower CLI
* https://tower-cli.readthedocs.io/en/latest/index.html
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

Backup/restore
```shell
tower-cli version > /awx_backup/version.txt
docker exec awx_postgres pg_dump -U awx -F t awx > /awx_backup/awx_backup.sql
# JSON version just in case (it is missing statistics, logs and some credential info)
tower-cli receive --all > /awx_backup/assets.json

# Restore
# Install correspondent version and wait for migration to complete
docker cp /awx_backup/awx_backup.sql awx_postgres:/tmp/awx_backup.sql
docker exec awx_postgres sh -c "pg_restore -U awx -c -d awx /tmp/awx_backup.sql"
```
