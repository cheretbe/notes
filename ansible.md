```yaml
- name: Add ACME account
  vars:
    # [!!!!] very creative
    acme_url: "https://acme{{ '-staging' if acme_staging else '' }}-v02.api.letsencrypt.org/directory"
  ansible.builtin.command: >
    pvesh create /cluster/acme/account
    --contact {{ acme_email }}
    --directory {{ acme_url }}
    --name {{ acme_account_name }}
    --tos_url {{ tos_url.stdout }}
  when: "acme_account_name not in acme_accounts.stdout | from_json | json_query('[].name')"
```
* :warning: Built-in Jinja filters: https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters
* :warning: Mitogen for Ansible: https://mitogen.networkgenomics.com/ansible_detailed.html
* VMware vSphere Automation SDK: https://github.com/vmware/vsphere-automation-sdk-python
    * Used in https://github.com/ansible-collections/community.vmware
* Review when time permits: https://github.com/ekultails/rootpages/blob/master/src/automation/ansible.rst
* :warning: Five Ansible Techniques I Wish I'd Known Earlier: https://zwischenzugs.com/2021/08/27/five-ansible-techniques-i-wish-id-known-earlier/
    * https://www.reddit.com/r/ansible/comments/pd8erk/five_ansible_techniques_i_wish_id_known_earlier/haoslej?utm_source=share&utm_medium=web2x&context=3
        * https://www.reddit.com/r/ansible/comments/pa9vew/run_a_playbook_depending_on_the_output_of_two/ha39y5a
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
* Color when there is no pty (CI/CD pipelines): https://www.jeffgeerling.com/blog/2020/getting-colorized-output-molecule-and-ansible-on-github-actions-ci

### Ad-Hoc Commands
```shell
# Default for category_names is ['Critical Updates','Security Updates','Update Rollups']
ansible win10 -m win_updates

ansible win10 -m win_updates \
  -a "category_names=['Critical Updates','Security Updates','Update Rollups','Updates','Definition Updates','Drivers'] reboot=yes"

ansible win10 -m community.windows.win_certificate_info -a 'store_name=Root'
# View single certificate info
ansible win10 -m community.windows.win_certificate_info -a 'store_name=Root thumbprint=0000000000000000000000000000000000000000'

ansible win10 -m win_certificate_store -a 'path=\\\\hostname\\path\\to\\self-signed-ca.cert.crt store_name=Root'

ansible win10 -m win_reg_stat -a "path='HKLM:\System\CurrentControlSet\Control\Session Manager' name=PendingFileRenameOperations"

# Deny interactive logon for ansible user
ansible win10 -m win_user_right -a "name=SeDenyInteractiveLogonRight action=add users=ansible-user"
# Deny logon through Remote Desktop Services for ansible user
ansible win10 -m win_user_right -a "name=SeDenyRemoteInteractiveLogonRight action=add users=ansible-user"
```

### Installation

```bash
/usr/bin/curl -s https://raw.githubusercontent.com/cheretbe/bootstrap/master/setup_venv.py?flush_cache=True \
  | /usr/bin/python3 - ansible --python 3.8

grep -qxF '. ~/.cache/venv/ansible/bin/activate' ~/.bashrc || \
  echo -e '\n. ~/.cache/venv/ansible/bin/activate\n' >>~/.bashrc

. ~/.cache/venv/ansible/bin/activate

pip install ansible pywinrm
```
:warning: A fix for `ntlm: unsupported hash type md4` error in newer versions of Python and OpenSSL. Edit existing `/usr/lib/openssl.cnf` or `/etc/ssl/openssl.cnf` (Ubuntu), merging the following into it:
```
[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```
* https://stackoverflow.com/questions/69938570/md4-hashlib-support-in-python-3-8
* https://bugs.launchpad.net/ubuntu/+source/python3.10/+bug/1971580/comments/3

### Client setup
```powershell
$ansiblePwd = Read-Host -AsSecureString
New-LocalUser -Name ansible-user -Password $ansiblePwd  -Description "Ansible user" -AccountNeverExpires -PasswordNeverExpires

Add-LocalGroupMember -Group "Администраторы" -Member "ansible-user"

# Deny interactive logon and remote desktop for ansible user
# === option 1 ===
Invoke-WebRequest https://raw.githubusercontent.com/cheretbe/bootstrap/master/ntrights.exe -OutFile ntrights.exe

# If Invoke-WebRequest fails with "Could not create SSL/TLS secure channel" message 
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

./ntrights.exe -u ansible-user +r SeDenyInteractiveLogonRight
./ntrights.exe -u ansible-user +r SeDenyRemoteInteractiveLogonRight
# ================
```
```shell
# Deny interactive logon and remote desktop for ansible user
# === option 2 ===
ansible win10 -m win_user_right -a "name=SeDenyInteractiveLogonRight action=add users=ansible-user"
ansible win10 -m win_user_right -a "name=SeDenyRemoteInteractiveLogonRight action=add users=ansible-user"
# ================
```

### Templates

```yaml
# Generated by Ansible at {{ lookup('pipe', 'hostname -f') }}
# Any changes made here will be overwritten
```

### Config
* https://docs.ansible.com/ansible/latest/reference_appendices/config.html
Local config: `~/.ansible.cfg`

### Inventory
* https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
* https://docs.ansible.com/ansible/latest/plugins/inventory.html#inventory-plugins
```shell
ansible-inventory -i demo.aws_ec2.yml --graph
# List all vars for a single host
ansible -m debug -a "var=hostvars[inventory_hostname]" host.domain.tld
```
* `export ANSIBLE_HOST_KEY_CHECKING=False` while you're deploying new servers, then remove it with `unset ANSIBLE_HOST_KEY_CHECKING`.
* or add to `/etc/ansible/ansible.cfg` or `~/.ansible.cfg`:
```
[defaults]
host_key_checking = False
```
* see also: https://stackoverflow.com/questions/23074412/how-to-set-host-key-checking-false-in-ansible-inventory-file


`ansible_virtualization_role`, `ansible_virtualization_type`
 * https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/facts/virtual/linux.py
 

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
#                         Multiple patterns: --limit '*AA*:*BB*:*CC*'
#                         for example: -l 'ubuntu-xenial:ubuntu-bionic'
# Run locally (note the trailing comma after 'localhost')
# -i localhost, --connection=local
ansible-playbook --connection=local -i localhost, playbook.yml
ansible localhost -m setup
ansible all -i machine_name, -m setup -u vagrant --ask-pass
ansible all -i ubuntu-bionic, -m setup -u vagrant -a "gather_subset=min" --extra-vars "ansible_password=vagrant"
ansible -m setup -a "filter=ansible_distribution_release" all
ansible cont-name -m setup -c docker -i cont-name,

# Access VM from Vagrant host
vagrant ssh-config
ansible all -m setup -i localhost, \
  --extra-vars "ansible_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key" \
  --extra-vars "ansible_port=2201"
# WinRM in Vagrant (not secure)
pip install pywinrm
ansible all -i 172.24.0.14, -m setup -u vagrant \
  --extra-vars "ansible_connection=winrm ansible_port=5985" \
  --extra-vars "ansible_winrm_transport=ntlm ansible_password=$AO_DEFAULT_VAGRANT_PASSWORD"
# WinRM from Vagrant host
vagrant winrm-config win-host-name
ansible all -i 127.0.0.1, -m setup -u vagrant \
  --extra-vars "ansible_connection=winrm ansible_port=55985" \
  --extra-vars "ansible_winrm_transport=ntlm ansible_winrm_scheme=http" \
  --extra-vars "ansible_password=$AO_DEFAULT_VAGRANT_PASSWORD"

# WinRM over SSL
ansible all -i host.domain.tld, -m setup -u user \
  --extra-vars "ansible_password=$WIN_PWD" \
  --extra-vars "ansible_connection=winrm ansible_winrm_transport=ntlm" \
  --extra-vars "ansible_winrm_ca_trust_path=/etc/ssl/certs"

read -s -p "Password: " ANSIBLE_PWD; echo ""; export ANSIBLE_PWD
ansible-playbook -i host.domain.tld, -u username check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3 ansible_password=$ANSIBLE_PWD"

pip install pywinrm
ansible-playbook -i host.domain.tld, -u user@domain.tld check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3" \
  --extra-vars "ansible_connection=winrm ansible_port=5985 ansible_winrm_transport=ntlm ansible_password=$ANSIBLE_PWD"

apt install libkrb5-dev
pip install wheel
pip install ansible pywinrm kerberos requests-kerberos pywinrm[kerberos]
# Client principal is case-sensitive. Use 'klist' to view
ansible-playbook -i host.domain.tld, -u user@DOMAIN.TLD check_if_reachable.yml \
  --extra-vars "ansible_python_interpreter=/usr/bin/python3" \
  --extra-vars "ansible_connection=winrm ansible_port=5985 ansible_winrm_transport=kerberos" \
  --extra-vars "ansible_winrm_kerberos_delegation=yes"

ansible-playbook -i container-name, --connection=docker \
  --extra-vars "ansible_user=ansible ansible_python_interpreter=/usr/bin/python3" \
  playbook.yml
```

Ad-hoc command returning JSON
```shell
# Permanent setting in config file:
# [defaults]
# stdout_callback = json
# bin_ansible_callbacks = True
# 
ANSIBLE_LOAD_CALLBACK_PLUGINS=true ANSIBLE_STDOUT_CALLBACK=json \
  ansible all -i 192.168.1.137, -a "ls / -lha" \
  | jq -r '.plays[0].tasks[0].hosts."192.168.1.137".stdout_lines'

# Show execution time for ad-hoc command
ANSIBLE_LOAD_CALLBACK_PLUGINS=true ANSIBLE_ENABLED_PLUGINS=timer ansible -i inventories/prod/linux.hosts -m ping hosts --one-line
```

```yaml
# Useful host variables

# Allows to connect using IP instead of host's name
ansible_host: 10.10.10.10
```
Interactive console
```shell
ansible-console -l host

setup
debug var="ansible_interfaces"
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

# SSH key generation
- name: Generate private key for user1 user
  community.crypto.openssl_privatekey:
    path: /home/user1/.ssh/id_rsa
    owner: user1
  become: yes

- name: Generate public key for user1 user
  community.crypto.openssl_publickey:
    format: OpenSSH
    path: /home/user1/.ssh/id_rsa.pub
    privatekey_path: /home/user1/.ssh/id_rsa
    owner: user1
    return_content: yes
  become: yes
  register: user1_pubkey

- debug:
    msg: "Public key: {{ user1_pubkey.publickey }}"
    
public_key_as_long_string___: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDG6\
  eY8ygJwZvRSEZKQU5clOu5s3aAH5swvD/tjIODCIW+XqFZn9o0qiDS7oOi27gBVP2gLRfj\
  dPKh69IXEWiHz+yAozc2rt5VyyM4Ej4ZCkj08vfOCoQGO0U2MXdGnjrg1cZcNEFN2zGa2l\
  tbdXyxY0DqV7R3Gzf96VpM9Bbpccb46wtoV/rSJZHJA1jUu9FV5cF/soRaJ95h6bynMo9L\
  ETleAkSHH9dm8Z4m6/PJB8DOnWg3J1eHL6n/a7s8SYdfZN2HmIiV+JmNojenKUtaUkgYum\
  gMcNhnXcKXUHpPPdjWB2LRGwI85nN3CtVpWbYARBcjvD0vqd5/wSyux7uiFbbdlSRxtNyX\
  qVUdHbai3r1Ih3I9XxC6MOdi8sznDJ+QA0gfnDg7/NL1Ir7nA3bBF3mqu1YgLKKIZMdDE5\
  2MhoHPepZiRubd1PYoo2kyS/dZsVBZf6mVjD2xd8o3jXnfms7j3qHaHtWVGHuNOcA3/jPt\
  6+YS2Nv0JfSqiysGvKb0= test key"
  
- name: Python3 test
  ansible.builtin.shell: |
    import json

    output ={
      "message": [],
      "changed": False
    }
    output["message"] += ["line 1"]
    output["message"] += ["line 2"]
    output["message"] += ["{{ my_ansible_variable }}"]

    print(json.dumps(output))
  args:
    executable: /usr/bin/python3
  register: test_result
  changed_when: (test_result.stdout|from_json).changed
  vars:
    my_ansible_variable: "dummy"

- debug:
    msg: "{{ (test_result.stdout|from_json).message }}"
  
- name: Powershell test 1
  ansible.windows.win_shell: |
    $output = [PSCustomObject]@{
      changed = (Get-Random -InputObject ([bool]$TRUE, [bool]$FALSE))
    }
    if ($output.has_message)
      { $output.message = "This is completely random" }
    $output | ConvertTo-Json
  register: test_result
  changed_when: (test_result.stdout|from_json).changed
  
- name: Powershell test 2
  ansible.windows.win_shell: |
    $output = [PSCustomObject]@{
      message = "";
      has_message = (Get-Random -InputObject ([bool]$TRUE, [bool]$FALSE))
    }
    if ($output.has_message)
      { $output.message = "This is completely random" }
    $output | ConvertTo-Json
  register: test_result
  changed_when: false

- name: Show message
  debug:
    msg: "Message: {{ (test_result.stdout|from_json).message }}"
  when: (test_result.stdout|from_json).has_message
  
- name: Powershell test 3
  ansible.windows.win_shell: |
    $output = [PSCustomObject]@{ changed=$FALSE; debug=@() }
    $output.debug += "test"
    $output | ConvertTo-Json
  register: test_result
  changed_when: (test_result.stdout|from_json).changed

- debug:
    var: (test_result.stdout|from_json).debug

```

##### Environment variables

The `env` lookup plugin returns an empty string when the requested environment variable is not set. `default()` will only return its first argument if the prior expression evaluates to `Undefined`. If you want to use the default value when variables evaluate to `false` or an empty string you have to set the second parameter to `true`.

```shell
# This will return "default"
ansible all -i localhost, --connection=local -m debug -a "msg={{ lookup('env', 'DUMMY') | default('default', true) }}"
# This will return ""
ansible all -i localhost, --connection=local -m debug -a "msg={{ lookup('env', 'DUMMY') | default('default') }}"
```
* https://docs.ansible.com/ansible/latest/collections/ansible/builtin/env_lookup.html
* https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#providing-default-values
* https://nikhilism.com/post/2016/understanding-ansible-jinja2-default-filter/

### Vault

* :warning: https://www.golinuxcloud.com/ansible-vault-example-encrypt-string-playbook/
* https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults
* Working with ansible-vault: https://gist.github.com/tristanfisher/e5a306144a637dc739e7
* https://serverfault.com/questions/878320/how-to-use-existing-vault-files-in-ansible-tower/935778#935778
    * https://github.com/AlanCoding/Ansible-inventory-file-examples/tree/master/vault/single_var_file
* https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#vault

```shell
# [!] It uses 'vault_password_file' option from .ansible.cfg if set
# [!!!] use space to prevent the command showing up in the history
ansible-vault encrypt_string 'string-value' --name 'parameter-name'

# Vault password as an env variable:
--vault-password-file vault_env_pass_file.sh
```
`vault_env_pass_file.sh` contents (make sure it is executable)
```bash
#!/bin/bash
echo ${ANSIBLE_VAULT_PASSWORD}
```
`.ansible.cfg` entry example:
```
[defaults]
vault_password_file = ~/vault_env_pass_file.sh
```

### Molecule
* https://ansible.readthedocs.io/
    * https://ansible.readthedocs.io/projects/molecule/guides/sharing/#sharing-across-scenarios
    * https://ansible.readthedocs.io/projects/molecule/configuration/
* Pugins: https://github.com/ansible-community/molecule-plugins

#### Lint
Molecule doesn't have lint command anymore: https://github.com/ansible/molecule/pull/3802
```shell
# The workaround is to run it manually
pip install ansible-lint yamllint
yamllint . --config-data "{extends: default, rules: {line-length: disable, quoted-strings: {quote-type: double, required: false}}}"
ansible-lint .
# Permanent yamllint config
cat > .yamllint<< EOF
---
extends: default
rules:
  line-length: disable
  quoted-strings:
    quote-type: double
    required: false
  # https://ansible.readthedocs.io/projects/lint/rules/yaml/
  comments:
    min-spaces-from-content: 1
  comments-indentation: false
  braces:
    max-spaces-inside: 1
  octal-values:
    forbid-implicit-octal: true
    forbid-explicit-octal: true
EOF
```

#### Vagrant

```shell
# Replace linux-provision/default with relevant path
# Ansible config contain useful settings like `host_key_checking = False`, `interpreter_python = auto_silent` etc.
ANSIBLE_CONFIG=~/.cache/molecule/linux-provision/default/ansible.cfg \
  ansible -i ~/.cache/molecule/linux-provision/default/inventory/ansible_inventory.yml \
   -m ping --become all

cd ~/.cache/molecule/linux-provision/default
vagrant snapshot save initial-state
```

```shell
# [!] Use correct extension pack version
VBoxManage --version
# As root
VBoxManage extpack install --replace Oracle_VM_VirtualBox_Extension_Pack-7.0.22.vbox-extpack

cd ~/.cache/molecule/linux-provision/default/
vboxmanage showvminfo $(cat .vagrant/machines/ubuntu-24.04.local.test/virtualbox/id) --machinereadable | grep vrdeport=

# on the client (select "Current KRDC Size", empty user name)
krdc rdp://host.domain.tld:5992
```

```yaml
---

driver:
  name: vagrant
platforms:
  # change_host_name in VagrantPlugins::ProviderVirtualBox::Provider correctly sets FQDN in /etc/hosts when
  # host.domain.tld name format is used
  - name: ubuntu-22.04.local.test
    box: ubuntu/jammy64
  # Canonical will no longer publish Vagrant images directly starting with Ubuntu 24.04 LTS (Noble Numbat)
  # https://documentation.ubuntu.com/public-images/en/latest/public-images-explanation/vagrant/#support
  # https://github.com/chef/bento
  - name: ubuntu-24.04.local.test
    box: bento/ubuntu-24.04
    memory: 512
    cpus: 1
    provider_raw_config_args:
      - "customize ['modifyvm', :id, '--vrdeaddress', '0.0.0.0']"
```


```shell
# [!] Need to specify ansible explicitly to get a fully functional ansible
pip install ansible molecule molecule-plugins[docker]
# pip install molecule ansible-lint flake8 molecule-vagrant
# Initialize Molecule within an existing role
cd role-directory
# if scenario-name is empty, 'default' is used
molecule init scenario [scenario-name]
molecule init scenario -d vagrant

molecule --base-config ../tests/molecule/molecule_base_docker_linux.yml test
```

`molecule.yml` example
```yaml
dependency:
  name: galaxy
driver:
  name: podman
platforms:
  - name: gitlab
    image: docker.io/gitlab/gitlab-ce:16.2.5-ce.0
    pre_build_image: true
    network: gitlab-test
    override_command: false
    published_ports:
      - "8000:8000"

  - name: debian-10
    image: docker.io/geerlingguy/docker-debian10-ansible:latest
    pre_build_image: true
    command: /lib/systemd/systemd
    network: gitlab-test

  - name: debian-11
    image: docker.io/geerlingguy/docker-debian11-ansible:latest
    pre_build_image: true
    command: /lib/systemd/systemd
    network: gitlab-test
provisioner:
  name: ansible
  playbooks:
    prepare: ../playbooks/prepare.yml
    cleanup: ../playbooks/cleanup.yml
  ansible_args:
    - --vault-password-file=molecule/ansible_vault_env_pass_file.sh
    - --extra-vars
    - "gl_debug_skip_test_docker_machine_vm=${MOLECULE_SKIP_TEST_VM:-false}"
  config_options:
    defaults:
      # These settings are for set_fact's cacheable parameter to work. This way
      # we can use test_project_info variable from prepare.yml in converge.yml
      gathering: smart
      fact_caching: jsonfile
      fact_caching_connection: /tmp/molecule_facts_cache
      fact_caching_timeout: 43200 #12h
verifier:
  name: ansible
```
### Testinfra

* :warning: 2review: https://medium.com/@george.shuklin/testinfra-pytest-delights-3e0a7d5c84d2

```shell
py.test --connection=ansible ./tests/
py.test --hosts=somehost --ansible-inventory=inventory --connection=ansible ./tests/
```

Testinfra interactive example
```python
import testinfra

# https://testinfra.readthedocs.io/en/latest/backends.html
# SSH backend
host = testinfra.get_host(
  "ssh://vagrant@localhost:2203",
  ssh_identity_file="/home/user/.cache/molecule/linux-dns/default/.vagrant/machines/ubuntu-bionic/virtualbox/private_key",
  ssh_extra_args="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
)

# Docker
host = testinfra.get_host("docker://cont_name")
# Or as a specific user
host = testinfra.get_host("docker://user@cont_name")

# Ansible
host = testinfra.get_host("ansible://host?ansible_inventory=/etc/ansible/inventory")
print(host.ansible("setup")["ansible_facts"]["ansible_virtualization_role"])

print(host.check_output("hostname -f"))
# [!] Use run only if a comand may fail, otherwise use check_output
print(host.run("hostname -f").stdout)
host.file("/etc/passwd").mode
host.socket("tcp://0.0.0.0:22").is_listening
host.socket.get_listening_sockets()
host.system_info.codename
host.system_info.distribution

if host.backend.HAS_RUN_ANSIBLE:
    pprint(host.ansible.get_variables())
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
### Custom modules
* https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#developing-modules-general
    * https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html
    * https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html#developing-modules-best-practices
    * https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html#developing-python-3
* https://vincent.bernat.ch/en/blog/2020-custom-ansible-module
    * https://vincent.bernat.ch/en/blog/2020-syncing-mysql-tables-ansible
    * https://github.com/vincentbernat/ansible-custom-module-examples/blob/main/mysql_import.py
* :bulb: 2check: https://docs.ansible.com/ansible/latest/dev_guide/developing_module_utilities.html#standard-module-utilities
* ❔ Utilize the testing tools in `ansible/hacking/`: `test-module`, `ansible-test sanity <MODULE_NAME>`
* plugin examples
    * https://github.com/ansible-collections/ansible.windows/blob/main/plugins/action/win_updates.py
    * https://github.com/ericwang984/portable-dc/blob/master/infra/packer/provision/roles/libraries/module_utils/action_runner.py
    * https://github.com/amtega/ansible_role_tower/blob/master/action_plugins/tower_setup_virtualenv.py
    * https://github.com/sbitio/ansible-sbhell/blob/develop/action_plugins/sbhell.py
    * https://github.com/ansible-network/network-engine/blob/devel/action_plugins/cli.py
    * https://github.com/limepepper/ansible-role-apache/blob/devel/action_plugins/apache_vhost_ssl.py
    * https://gist.github.com/ju2wheels/408e2d34c788e417832c756320d05fb5
    * https://github.com/phlummox/ansible-dokku-vouch-provisioner/blob/master/ansible-lib/plugins/action/dokku_push.py
    * https://github.com/epfl-si/ansible-module-openshift/blob/master/action_plugins/openshift_imagestream.py
