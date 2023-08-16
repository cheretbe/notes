* https://linux.die.net/man/5/sshd_config
* https://linux.die.net/man/5/ssh_config

On server in `/etc/ssh/sshd_config`:
```
# Multiple environment variables may be separated by whitespace or spread across multiple AcceptEnv directives
AcceptEnv VAR1 VAR2
AcceptEnv VAR3
```
On client in `/etc/ssh/ssh_config`:
```
# Multiple environment variables may be separated by whitespace or spread across multiple SendEnv directives
Host hostname
    SendEnv VAR1 VAR2 VAR3
```

### Host keys
```shell
ls /etc/ssh/ssh_host_*_key*
```
 
### Hardening SSH Access
SSH daemon options in `/etc/ssh/sshd_config`:
```
PermitRootLogin no
# [!!!] Authentication key-pair must be created and tested beforehand
PasswordAuthentication no
# [!!!] If SELinux is enabled, SSH daemon needs to be allowed to listen on a new port
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
Port <port_number>
```

### Reverse SSH Tunnel

#### On server
Create [an additional instance](#multiple-instances-of-sshd) of sshd. Restrict allowed options in `/etc/ssh/sshd_config_rev_tunnel`
```
# Set this option to use IPv4 only (and to suppress error: bind: Cannot assign requested address)
AddressFamily inet

AllowTcpForwarding yes
X11Forwarding no
PermitTunnel no
PermitTTY no
#GatewayPorts no
#GatewayPorts clientspecified
GatewayPorts yes
AllowAgentForwarding no
ForceCommand echo 'This service can only be used for reverse port forwarding'
# PermitOpen locahost:1234
# PermitOpen restricts only *local* port forwarding
# For remote ports PermitListen option has been added, but it is not supported by most
# versions of sshd
# https://bugzilla.mindrot.org/show_bug.cgi?id=2038
ClientAliveInterval 60
ClientAliveCountMax 5
```
* https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Tunnels
#### On client
```bash
# Test tunnel creation
ssh -v -i keys/tunnel-user-key.key tunnel-user@host.domain.tld -p 12345 -N -R 1234:localhost:22
```

Install `supervisord` and create `/etc/supervisor/conf.d/reverse-ssh-tunnel.conf` file with the following contents
```apache
[program:reverse-ssh-tunnel]
environment=AUTOSSH_GATETIME=0

# -M 0  monitoring port (do not monitor)
# -N    do not execute a remote command, just forward ports
# -T    disable pseudo-tty allocation
# -v    verbose mode
# Additional parameters are in /home/local-user/.ssh/config (remote-tunnel)
command=/usr/bin/autossh -v -M 0 -N -T remote-tunnel

user=local-user
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/reverse-ssh-tunnel.log
redirect_stderr=true
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=3
```

`/home/local-user/.ssh/config` contents
```
Host remote-tunnel
  Hostname               host.domain.tld
  ServerAliveInterval    30
  ServerAliveCountMax    3
  PubkeyAuthentication   yes
  PasswordAuthentication no
  ExitOnForwardFailure   yes
  IdentityFile           /home/local-user/keys/tunnel-user-key.key
  User                   tunnel-user
  Port                   12345
  RemoteForward          1234 localhost:22
  RemoteForward          1235 192.168.1.8:443
  ServerAliveInterval    30
  ServerAliveCountMax    3
```
```bash
# Enable and start supervisord service
systemctl enable supervisor.service
service supervisor start

# Reverse tunnel service control
supervisorctl stop reverse-ssh-tunnel
supervisorctl start reverse-ssh-tunnel

# Re-read changed config and restart the service without affecting other services
supervisorctl reread
supervisorctl update
```


### Multiple instances of sshd

#### Systemd (Centos 7, Debian 8, Ubuntu 16.04)

```
ln -s /usr/sbin/sshd /usr/sbin/sshd-external
```

* Make a copy of the systemd unit file for the sshd service
```shell
cp /usr/lib/systemd/system/sshd{,-external}.service
# debian/ubuntu
cp /lib/systemd/system/ssh{,-external}.service
```

* Modify `sshd-external.service` file
```shell
vi /usr/lib/systemd/system/sshd-external.service
# debian/ubuntu
vi /lib/systemd/system/ssh-external.service
```
```apache
# modify Description
Description=OpenSSH server daemon (external)
# modify After: add sshd.service, so that the second instance starts only after the first
# one has started (which includes key generation), remove sshd-keygen.service
After=network.target sshd.service
# debian/ubuntu
After=network.target ssh.service
# modify ExecStart (add -f /etc/ssh/sshd_config_external)
ExecStart=/usr/sbin/sshd-external -D -f /etc/ssh/sshd_config_external $SSHD_OPTS

# 18.04
ExecStartPre=/usr/sbin/sshd-external -t -f /etc/ssh/sshd_config_external
ExecReload=/usr/sbin/sshd-external -t -f /etc/ssh/sshd_config_external
RuntimeDirectory=sshd-external

# debian/ubuntu only
[Install]
Alias=sshd-external.service
```

* Make a copy of the sshd_config file 
```
cp /etc/ssh/sshd_config{,_external}
```

* Edit 'sshd_config_external' to assign a different port number and PID file
```
vi /etc/ssh/sshd_config_external
```
```
Port 22220
# Uncomment or add
PidFile /var/run/sshd-external.pid
```

If login fails with `fatal: Access denied for user username by PAM account configuration [preauth]` message, make a copy of the PAM configuation file
```
cp /etc/pam.d/sshd{,-external}
```

Enable service start on boot
```shell
systemctl enable sshd-external
# debian/ubuntu
systemctl enable ssh-external
```

Turn on debugging if daemon fails to load
Add `-ddd` option to `/etc/sysconfig/sshd` (debian `/etc/default/ssh`)
```
SSHD_OPTS=-ddd
```

Re-read systemctl configuration if .service file is modified after start attempt
```
systemctl daemon-reload
```

https://access.redhat.com/solutions/1166283

### SSH Keys

```shell
# https://security.stackexchange.com/questions/143442/what-are-ssh-keygen-best-practices/144044#144044
# https://medium.com/risan/upgrade-your-ssh-key-to-ed25519-c6e8d60d3c54
ssh-keygen -t ed25519 -a 100 -C "test-comment" -f keys/my_key
ln -s ~/keys/my_key .ssh/id_ed25519
ln -s ~/keys/my_key.pub .ssh/id_ed25519.pub

# [!] Don't use this, see above
ssh-keygen -C "test-comment" -f test.key
# View the fingerprint
ssh-keygen -lf key_file
# Retrieve the public key
ssh-keygen -yf key_file

# [!!] Use -i option to prevent accidental id_rsa.pub copying
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host
```
To add a comment in `authorized_keys` just use a space and a comment after the key:
```
ssh-dss AAAAB3N...JjHIvNsBk= ThisIsAComment
```

* https://wiki.archlinux.org/index.php/SSH_keys#Choosing_the_authentication_key_type

#### ssh-agent
```shell
#  List fingerprints of all identities currently represented by the agent
ssh-add -l
```

```
Host example
  ForwardAgent yes

Host *.domain.tld
  ForwardAgent yes
```

### Mount a remote SSH directory
```shell
sudo apt install sshfs
# Create the mount point
mkdir ~/yourmountdirectory
# Mount remote path
sshfs -o reconnect username@host:/remotepath ~/yourmountdirectory
# As root
sshfs -o sftp_server="/usr/bin/sudo /usr/lib/openssh/sftp-server" -o reconnect host.domain.tld:/ ~/yourmountdirectory
# Unmount
fusermount -u ~/yourmountdirectory
# View mounted filesystems
mount -t fuse.sshfs
```

### Notes
Custom connection options
```
touch ~/.ssh/config
```
```
Host host1
  HostName host1.domain.tld
  User username
  Port 1234
  IdentityFile /path/to/a/file
  ForwardX11 yes
  LocalForward 2345 192.168.0.1:3389
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  ServerAliveInterval    30
  ServerAliveCountMax    3
```


```bash
# RDP port forwarding
ssh user@host.tld -L 1234:192.168.0.200:3389
# Don't check host key and don't add it to known_hosts
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@host.tld
```

``` bash
# Find out PIDs of active tunnels
netstat -tulpn | grep sshd
```
`/etc/ssh/sshd_config` options
```apache
# To fix X11 forwading error
X11UseLocalHost no
# Allow port forwading
AllowTcpForwarding yes
```
```shell
# Keeping X11 display after su or sudo
# For non-root accounts list authority file contents BEFORE su
xauth -f ~/.Xauthority list
# Note the last line, e.g:
# host.domain.tld:10  MIT-MAGIC-COOKIE-1  75260434b52f448f9e21e0cf8c694102
# After su add the same entry for a new user
xauth add host.domain.tld:10  MIT-MAGIC-COOKIE-1  75260434b52f448f9e21e0cf8c694102

# For root the following one-liner is enough
xauth add $(xauth -f ~john/.Xauthority list|tail -1)
```
Do not forward the locale settings
* on client: in `/etc/ssh/ssh_config` comment out the line:
```
#SendEnv LANG LC_*
```
Can't be disabled in `~/.ssh/config` (https://superuser.com/questions/485569/how-to-disable-sendenv-variables-set-in-ssh-config-from-ssh-config)

* on server: in `/etc/ssh/sshd_config` comment out the line:
```
#AcceptEnv LANG LC_*
```
