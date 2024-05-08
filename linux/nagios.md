* https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html#host
* https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html#hostgroup
* https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html#service

Note on the following error:
```
Error: (use_ssl == true): Request packet version was invalid!
Could not read request from client , bailing out...
```
Just ignore it if `check_nrpe` call result is not timeout. View other logs, check file permissions and sudoers settings first.


* https://unweb.me/blog/nagios-clients-behind-paranoid-firewalls
* https://www.techrepublic.com/blog/linux-and-open-source/remotely-monitor-servers-with-the-nagios-check-by-ssh-plugin/

```shell
# Check SSL certificate expiration
/usr/local/nagios/libexec/check_http --ssl -H reddit.com -C 100
#define command{
#        command_name    check_ssl_cert
#        command_line    $USER1$/check_http --ssl -H $HOSTADDRESS$ -C $ARG1$
#}
```

### Docker
* `manios/nagios:latest`
  
`/etc/ssmtp/ssmtp.conf` example
```
# https://linux.die.net/man/5/ssmtp.conf
# The user that gets all mail for userids less than 1000. If blank, address rewriting is disabled.
root=notifications@domain.tld
mailhub=mail.domain.tld
hostname=nagios-docker
```

```shell
docker exec -it nagios bash
# /opt/nagios/etc
cat etc/nagios.cfg
docker exec -it nagios bin/nagios -v etc/nagios.cfg
docker exec -it nagios libexec/check_nrpe -H host.domain.tld -c check_root
```

### Client (monitored host)

```bash
apt install nagios-plugins nagios-nrpe-server
cp /etc/nagios/nrpe.cfg{,.bak}
nano /etc/nagios/nrpe.cfg
# Configure Allowed Hosts
# allowed_hosts=127.0.0.1, nagios.domain.tld

# command[check_root]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /
# command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 20 -c 10

service nagios-nrpe-server restart

# On server
/usr/local/nagios/libexec/check_nrpe -H host.domain.tld -c check_root
/usr/local/nagios/libexec/check_nrpe -H host.domain.tld -c burp_user_status -a hostname 1440 2880
```
Custom plugins: https://github.com/cheretbe/nagios-plugins

Allowing nrpe command arguments is in the old readme.

### Server config

* Default installation path: `/usr/local/nagios/`
* Default config path: `/usr/local/nagios/etc/`
* Log location: `/usr/local/nagios/var/nagios.log`

Add the folowing lines to `/usr/local/nagios/etc/nagios.cfg`
```
cfg_file=/usr/local/nagios/etc/hosts.cfg
cfg_file=/usr/local/nagios/etc/services.cfg
```
and configure hosts and services.

**Tip:** Start out by creating profiles for both services and hosts, then assign your hosts to the profiles (hostgroups?) as opposed to taking a host and applying a group of services to that host. If you do it this way, your life will be much easier. If you build the profiles first, then to add a new host you just drop it into a profile and all of the service checks will be added. If you update a service profile then all hosts that use that profile will get the new service check.

**Tip:** Create custom versions of files in `/usr/local/nagios/etc/objects` and inculde them in `nagios.cfg` with `cfg_file` directive
```
cfg_file=/usr/local/nagios/etc/objects/custom-commands.cfg
```

```bash
# Check config after editing
 /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
```

**Debugging:**<br> Set `debug_level` parameter (see comments in `/usr/local/nagios/etc/nagios.cfg`), then check `/usr/local/nagios/var/nagios.debug` contents.

If "Error: Could not stat() command file '/usr/local/nagios/var/rw/nagios.cmd'!" error pops up and the group for `nagios.cmd` is already `nagcmd`, **check selinux status**
```shell
chown nagios:nagcmd /usr/local/nagios/var/rw
chown nagios:nagcmd /usr/local/nagios/var/rw/nagios.cmd
```
Client:<br>
* https://www.lowlevelmanager.com/2012/05/debugging-nagios-remote-nrpe-commands.html
    * check env:
    ```
    define commands:
    command[check_ui_test]=whoami
    command[check_ui_test2]=env
    the run:
    check_nrpe -H 10.7.202.92 -c check_ui_test
    check_nrpe -H 10.7.202.92 -c check_ui_test2
    ```

## Installation
* https://support.nagios.com/kb/article.php?id=96

![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) Don't install sendmail if postfix is already installed
```bash
apt install build-essential apache2 php apache2-mod-php7.0 php-gd libgd-dev libssl-dev sendmail unzip
# Set up the users and groups which Nagios expects
# These are in a few places in the default config; it’s not worth changing them
adduser nagios
addgroup nagcmd
usermod -a -G nagcmd nagios
usermod -a -G nagcmd www-data

mkdir -p source
cd source
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.3.1.tar.gz
wget https://nagios-plugins.org/download/nagios-plugins-2.1.4.tar.gz
wget https://github.com/NagiosEnterprises/nrpe/archive/3.0.1.tar.gz
tar xzvf nagios-4.3.1.tar.gz
tar xzvf nagios-plugins-2.1.4.tar.gz
tar xzvf 3.0.1.tar.gz

cd nagios-4.3.1/
# (?) /usr/sbin/sendmail or skip --with-mail altogether
./configure --with-command-group=nagcmd --with-mail=/usr/bin/sendmail --with-httpd-conf=/etc/apache2/
```
The following is for clean installation, for upgrade instructions see `Upgrade` section below.
```bash
make all
make install
#make install-init
make install-config
make install-commandmode
make install-webconf

cp -R contrib/eventhandlers/ /usr/local/nagios/libexec/
chown -R nagios:nagios /usr/local/nagios/libexec/eventhandlers

sudo a2ensite nagios
sudo a2enmod rewrite cgi

cp /etc/init.d/skeleton /etc/init.d/nagios
chmod +x /etc/init.d/nagios
nano /etc/init.d/nagios
```
Add/change the following lines:
```
DESC="Nagios"
NAME=nagios
DAEMON=/usr/local/nagios/bin/$NAME
DAEMON_ARGS="-d /usr/local/nagios/etc/nagios.cfg"
PIDFILE=/usr/local/nagios/var/$NAME.lock
```
```bash
systemctl daemon-reload
systemctl restart apache2
systemctl start nagios

# Create a Default User for Web Access
htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin

chown :nagcmd /usr/local/nagios/var/rw
chown :nagcmd /usr/local/nagios/var/rw/nagios.cmd
```

### Upgrade
```bash
nagios_version=($(curl -s "https://www.nagios.org/checkforupdates/?product=nagioscore"| grep -Eo "is [0-9]{1}\.[0-9]{1}\.[0-9]{1}"))
nagios_version=${nagios_version[1]}
echo $nagios_version

plugins_version=($(curl -s "https://www.nagios.org/downloads/nagios-plugins/"| grep -Eo "Plugins [0-9]{1}\.[0-9]{1}\.[0-9]{1}"))
plugins_version=${plugins_version[1]}
echo $plugins_version

mkdir -p ~/source
cd ~/source
wget "https://assets.nagios.com/downloads/nagioscore/releases/nagios-${nagios_version}.tar.gz"
wget "https://nagios-plugins.org/download/nagios-plugins-${plugins_version}.tar.gz"

tar xzf nagios-${nagios_version}.tar.gz
tar xzf nagios-plugins-${plugins_version}.tar.gz

systemctl stop nagios.service

cd nagios-${nagios_version}
./configure
make all
make install
#make install-init
#make install-commandmode
#make install-config
#make install-webconf
#make install-exfoliation

cd ../nagios-plugins-${plugins_version}
./configure
make all
make install

systemctl start nagios.service
```

### Nagios plugins Installation

(?) `--with-openssl=/usr/bin/openssl` option is needed on Ubuntu. Check for CentOS (can be /bin/openssl or /usr/bin/openssl - check in script). Or update OPENSSL_DIRS in `configure`?
* https://community.spiceworks.com/topic/145769-ssl-is-not-available-error-when-using-check_http
* https://github.com/nagios-plugins/nagios-plugins/issues/174
```bash
cd ../nagios-plugins-2.1.4
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
make install

cd ../nrpe-3.0.1
./configure
make all
make install-plugin
```

* https://assets.nagios.com/downloads/nagioscore/docs/Installing_Nagios_Core_From_Source.pdf
* https://assets.nagios.com/downloads/nagioscore/docs/Nagios-Core-Installing-On-Centos7.pdf
* http://idroot.net/linux/install-nagios-ubuntu-16-04/
* http://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/install-nagios-4-1-1-ubuntu-16-04.html
* ~~https://jamieduerden.me/post/monitoring-nginx-nagios/~~
* ~~http://www.bogotobogo.com/DevOps/DevOps_Nginx_Nagios-Remote-Plugin-Executor-NRPE.php.NOT-Working~~

### Remote SSH host monitoring 

`/usr/local/nagios/etc/hosts.cfg`
```
define host {
        name                    custom-remote-server
        use                     generic-host
        max_check_attempts      5
        check_command           check_host_alive_ssh!--port=12345
        contact_groups          admins
        notification_interval   1140            ; 24h
        register                0               ; DON'T REGISTER, THIS IS A TEMPLATE
}
```

`/usr/local/nagios/etc/services.cfg`
```
define service {
        use                     custom-service
        hostgroup_name          custom-linux-remote-servers
        service_description     CPU Load
        check_command           remote_check_by_ssh!/usr/lib/nagios/plugins/check_load -w 15,10,5 -c 30,25,20!12345
}

```

`/usr/local/nagios/etc/commands.cfg`
```
define command {
        command_name    check_host_alive_ssh
        command_line    $USER1$/check_ssh $ARG1$ $HOSTADDRESS$
}
define command {
        command_name    remote_check_by_ssh
        command_line    $USER1$/check_by_ssh -H $HOSTADDRESS$ -C "$ARG1$" -p $ARG2$
}
```
