* logs are in `/var/log/cloud-init.log`
* some data (?) are in `/var/lib/cloud`

`preserve_sources_list` gotcha:
```yaml
# 'preserve_sources_list' repeated twice is intentional. There is a bug in cloud-init where it tries to
# reconcile the two settings as if they're different and fails with the following error:
#   Old and New apt format defined with unequal values False vs True @ apt_preserve_sources_list
# So we can't just use newer 'apt: {preserve_sources_list: true}' setting
apt_preserve_sources_list: true
apt:
  preserve_sources_list: true
```

```shell
# [!] Note \EOF - escapes dollar signs
cat <<\EOF >/tmp/os_user_data
#cloud-config
timezone: Europe/Moscow
fqdn: host.domain.tld
users:
  - name: cheretbe
    groups: [sudo]
    lock-passwd: false
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    # mkpasswd -m sha512crypt
    passwd: "$6$r/5YeV6tiWItqFyh$/xq8F4IkwgARQCbdH5A7mmWn8wbk.QsbH.jnsvaoNFtBvVLT5RSDiJ0NXjCz/M7AsnVMTvXZ5MlrjjvVxvZvN/"
    ssh_authorized_keys:
      - "ssh-ed25519 0000000000000000000000000000000000000000000000000000000 cheretbe"
EOF
```
