* https://www.debian.org/doc/manuals/debian-reference/ch05.en.html#_the_hostname_resolution
* **https://serverfault.com/questions/331936/setting-the-hostname-fqdn-or-short-name**
* https://serverfault.com/questions/363095/why-does-my-hostname-appear-with-the-address-127-0-1-1-rather-than-127-0-0-1-in
* https://linuxconfig.org/how-to-change-hostname-on-ubuntu-18-04-bionic-beaver-linux


### Change host name
* Cloud-init uses own mechanism and can override settings
    * https://linuxize.com/post/how-to-change-hostname-on-ubuntu-18-04/
    * Disable cloud-init: `touch /etc/cloud/cloud-init.disabled`
#### Ubuntu
Assuming we are setting the name `new-name.domain.tld`
1. Edit `/etc/hostname` file and update **short name**:
```
new-name
```
2. Edit `/etc/hosts` and update both short and FQDN:
```
127.0.0.1	localhost
127.0.1.1	new-name.domain.tld	new-name
```
* `127.0.1.1` is a replacement for static IP address ([more details here](http://www.debian.org/doc/manuals/debian-reference/ch05.en.html#_the_hostname_resolution))
* If the host has a static IP, use it instead of `127.0.1.1`
3. Run `hostname new-name` or just reboot for good measure.
4. :question: Check if `/etc/cloud/cloud.cfg` settings affect the host name (vagrant, LXD, etc.)
* [This guide](https://linuxconfig.org/how-to-change-hostname-on-ubuntu-18-04-bionic-beaver-linux) suggests changing `preserve_hostname: false` (also here: https://linuxize.com/post/how-to-change-hostname-on-ubuntu-18-04/)
 to `preserve_hostname: true`
* `lxc move old-name new-name` doesn't seem to update anything in the container itself
5. If rename is the result of copying/cloning a VM make sure to also change the machine ID ([networking.md#dhcp](./networking.md#dhcp))

#### CentOS

* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec_configuring_host_names_using_hostnamectl

Use hostnamectl<br>
If rename is the result of copying/cloning a VM make sure to also change the machine ID ([networking.md#dhcp](./networking.md#dhcp))

```shell
vi /etc/hostname
vi /etc/hosts
# CentOS, check for HOSTNAME=value presence
vi /etc/sysconfig/network
hostname new-name
```

#### hostnamectl

The hostnamectl tool is provided for administering the three separate classes of host names in use on a given system. The three classes of hostname are: static, pretty, and transient.

The static host name is the traditional hostname, which can be chosen by the user, and is stored in the /etc/hostname file. The "transient" hostname is a dynamic host name maintained by the kernel. It is initialized to the static host name by default, whose value defaults to `localhost`. It can be changed by DHCP or mDNS at runtime. The pretty hostname is a free-form UTF8 host name for presentation to the user.

```
hostnamectl status
hostnamectl status --transient
hostnamectl status --static
hostnamectl status --pretty
hostnamectl set-hostname "host.domain.tld" --transient
hostnamectl set-hostname "host.domain.tld" --static
hostnamectl set-hostname "My Host" --pretty
```
