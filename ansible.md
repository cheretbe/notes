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


### Config
* https://docs.ansible.com/ansible/latest/reference_appendices/config.html
Local config: `~/.ansible.cfg`

### Inventory
* https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
* https://docs.ansible.com/ansible/latest/plugins/inventory.html#inventory-plugins
```shell
ansible-inventory -i demo.aws_ec2.yml --graph
```
* `export ANSIBLE_HOST_KEY_CHECKING=False` while you're deploying new servers, then remove it with `unset ANSIBLE_HOST_KEY_CHECKING`.
* see also: https://stackoverflow.com/questions/23074412/how-to-set-host-key-checking-false-in-ansible-inventory-file


```shell
read -s -p "Password: " TOWER_PASSWORD; echo ""; export TOWER_PASSWORD
# [!] inventory file has to have .tower.yml extension
# see ~/.ansible.cfg below to use without -i option
ansible-inventory -i my_inventory.tower.yml --graph --vars
```
`my_inventory.tower.yml`

```yml
---
plugin: tower
host: http://localhost
username: your_ansible_tower_username
#password: your_ansible_tower_password
inventory_id: Inventory%20Name%20With%20A%20Space++Organization%20Name
#validate_certs: False
```
`~/.ansible.cfg` example for AWX:
```
[defaults]
inventory=./awx_inventory.tower.yml
```

### Roles and playbooks

* https://galaxy.ansible.com/docs/finding/content_types.html#ansible-roles
* https://linuxacademy.com/blog/linux-academy/ansible-roles-explained/
* https://docs.ansible.com/ansible/latest/modules/blockinfile_module.html#examples
* https://docs.ansible.com/ansible/latest/user_guide/playbooks_blocks.html
* 15 Things You Should Know About Ansible: https://habr.com/ru/post/306998/
* **https://molecule.readthedocs.io/en/stable/**

```bash
# https://docs.ansible.com/ansible/latest/modules/setup_module.html#parameters
# --check                 Dry run
# --module-path /ansible-playbooks/library
# --limit ubuntu-xenial   Run only on selected hosts
# Run locally (note the trailing comma after 'localhost')
# -i localhost, --connection=local
ansible-playbook --connection=local -i localhost, playbook.yml
ansible localhost -m setup
ansible all -i machine_name, -m setup -u vagrant --ask-pass
ansible all -i ubuntu-bionic, -m setup -u vagrant -a "gather_subset=min" --extra-vars "ansible_password=vagrant"

read -s -p "Password: " ANSIBLE_PWD; echo ""; export ANSIBLE_PWD
ansible-playbook -i host.domain.tld, -u username check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3 ansible_password=$ANSIBLE_PWD"
  
pip install pywinrm
ansible-playbook -i host.domain.tld, -u user@domain.tld check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3" \
  --extra-vars "ansible_connection=winrm ansible_port=5985 ansible_winrm_transport=ntlm ansible_password=$ANSIBLE_PWD"

pip install kerberos requests-kerberos
# Client principal is case-sensitive. Use 'klist' to view
ansible-playbook -i host.domain.tld, -u user@DOMAIN.TLD check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3" \
  --extra-vars "ansible_connection=winrm ansible_port=5985 ansible_winrm_transport=kerberos"

ansible-playbook -i container-name, --connection=docker \
  --extra-vars "ansible_user=ansible ansible_python_interpreter=/usr/bin/python3" \
  playbook.yml
```

```yaml
# Useful host variables

# Allows to connect using IP instead of host's name
ansible_host: 10.10.10.10
```
Interactive debugging: https://docs.ansible.com/ansible/latest/user_guide/playbooks_debugger.html
```yaml
- name: Failed command example
  command: false
  debugger: on_failed
```

```yaml
- name: populate service facts
  service_facts:

- debug:
    var: ansible_facts.services

  when: some_fact_that_contains_a_string|bool
  
# In 2.5 version_compare was renamed to version
# This test also accepts a 3rd parameter, strict
- debug:
    msg: "{% if '1.05' is version('1.04', '<=') %} less-or-equal {%else%} not-less {%endif%}"
    when: "'10' is version('1.04', '<=')"
  
- name: Assertion
  assert:
    that:
      - result.images | length == 2
      
- name: Cancel
  fail:
    msg: "Debug"

# This ends playbook without any message at all
- name: Debug
  meta: end_play

# This shows both task name and message
- block:
  - name: Debug
    debug:
      msg: End playbook with a message
  - meta: end_play
```

### Vault

* https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults
* Working with ansible-vault: https://gist.github.com/tristanfisher/e5a306144a637dc739e7
* https://serverfault.com/questions/878320/how-to-use-existing-vault-files-in-ansible-tower/935778#935778
    * https://github.com/AlanCoding/Ansible-inventory-file-examples/tree/master/vault/single_var_file
* https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#vault

```shell
# [!] use space to prevent the command showing up in history
ansible-vault encrypt_string 'string-value' --name 'parameter-name'
```

### Molecule
* https://opensource.com/article/18/12/testing-ansible-roles-molecule
* https://molecule.readthedocs.io/en/latest/
* https://github.com/ansible-community/molecule
* https://groups.google.com/forum/#!forum/molecule-users
* **https://www.toptechskills.com/ansible-tutorials-courses/rapidly-build-test-ansible-roles-molecule-docker/**
* https://www.ansible.com/hubfs//AnsibleFest%20ATL%20Slide%20Decks/Practical%20Ansible%20Testing%20with%20Molecule.pdf
    * https://www.ansible.com/practical-ansible-testing-with-molecule
    * https://github.com/fabianvf/practical-testing-with-molecule
* **https://molecule.readthedocs.io/en/latest/examples.html**    
* https://redhatnordicssa.github.io/how-we-test-our-roles

-------
* https://github.com/ansible-community/molecule-vagrant
* :warning: https://github.com/ansible-community/molecule-lxd/issues/1
    * https://github.com/ansible-community/molecule/pull/2329
    
```shell
pip install molecule ansible-lint flake8 molecule-vagrant
# Initialize Molecule within an existing role
cd role-directory
# if scenario-name is empty, 'default' is used
molecule init scenario [scenario-name]
molecule init scenario -d vagrant
```

Default test matrix
* dependency
* lint
* cleanup
* destroy
* syntax
* create
* prepare
* converge
* idempotence
* side_effect
* verify
* cleanup
* destroy


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
# https://docs.ansible.com/ansible/latest/reference_appendices/interpreter_discovery.html
interpreter_python = auto
```
On managed machines
```
[py3-hosts:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Windows

* https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#inventory-options
* https://docs.ansible.com/ansible-tower/latest/html/administration/kerberos_auth.html

### AWX
* **Mailing list:** https://groups.google.com/forum/#!forum/awx-project
* **Changelog:** https://github.com/ansible/awx/blob/devel/CHANGELOG.md
* https://github.com/ansible/awx
* https://www.unixarena.com/2018/10/ansible-how-to-install-and-configure-awx.html/
* https://www.unixarena.com/2018/11/ansible-tower-awx-organization-team-users-hierarchy.html/

#### Upgrade
Just run the new installer
```diff
# No need to remove docker containers
- docker rm -f $(docker ps -a -q)
- docker rmi -f $(docker images | grep awx | awk '{ print $3 }')
```
```
# Review default inventory changes before installation
diff awx-6.1.0/installer/inventory awx-7.0.0/installer/inventory

# cleanup space after upgrade (/var/lib/docker/overlay2/)
sudo docker system prune -a -f
```
* https://github.com/ansible/awx/blob/devel/INSTALL.md#upgrading-from-previous-versions
* **https://github.com/ansible/awx/issues/5228**
* https://github.com/ansible/awx/blob/devel/installer/roles/local_docker/templates/docker-compose.yml.j2#L144

#### Installation
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
# If custom hosthame is needed
sed -i 's+awx_task_hostname=awx+awx_task_hostname=host.domain.tld+' /opt/awx/inventory
cat /opt/awx/inventory | grep -v "#" |sort -n | grep .
ansible-playbook -i /opt/awx/inventory awx-7.0.0/installer/install.yml
# Wait for migration to complete
docker logs -f awx_task

docker exec -ti awx_task /bin/bash
```
Installation troubleshooting
* Stuck on "AWX is Upgrading"
```shell
cd /opt/awx/awxcompose
docker-compose logs -f
# if there is an endless loop with message like this
# awx_task | psycopg2.ProgrammingError: relation "main_instance" does not exist

# Stop containers and re-run installer
docker-compose stop
ansible-playbook -i /opt/awx/inventory awx-7.0.0/installer/install.yml
```
* https://github.com/geerlingguy/ansible-vagrant-examples/issues/48#issuecomment-517740305

#### Uninstallation
```shell
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images | grep awx | awk '{ print $3 }')
rm -rf /opt/awx/awxcompose
rm -rf /opt/awx/pgdocker
```

#### Tower CLI
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
