* Specifiers (variables) list :https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Specifiers
   * e.g. `"%N"` - Full unit name without suffix


On CentOS systemctl commands may start failing after systemd update
* https://superuser.com/questions/1125250/systemctl-access-denied-when-root
```shell
# Send SIGTERM to the daemon running as PID 1
kill -TERM 1
```

```shell
# View all actual settings in effect for a unit
systemctl show service

systemctl --now enable service
systemctl --now disable service

# Find system boot-up performance statistics
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain

# List all services
systemctl list-unit-files --type=service --no-pager
# Only enabled
systemctl list-unit-files --type=service --state=enabled --no-pager

# List active services
systemctl --type=service --state=active
```

* Nginx
    * CentOS `/usr/lib/systemd/system/nginx.service`
    * Debian `/lib/systemd/system/nginx.service`

```shell
# list-units   List units that systemd currently has in memory
systemctl list-units libvirt-guests.service libvirtd.service qemu-kvm.service
# UNIT                   LOAD   ACTIVE SUB     DESCRIPTION                                  
# libvirt-guests.service loaded active exited  Suspend/Resume Running libvirt Guests        
# libvirtd.service       loaded active running Virtualization daemon                        
# qemu-kvm.service       loaded active exited  QEMU KVM preparation - module, ksm, hugepages

# list-unit-files  List unit files installed on the system, in combination with their
#                  enablement state (as reported by is-enabled)
systemctl list-unit-files libvirt-guests.service libvirtd.service qemu-kvm.service
# UNIT FILE              STATE   
# libvirt-guests.service disabled
# libvirtd.service       disabled
# qemu-kvm.service       enabled

# Check if service is enabled
systemctl is-enabled mysqld.service
# Enable service
systemctl enable mysqld.service
# Reload settings after editing a unit file
systemctl daemon-reload
```

Auto-start service after crash (See `Restart=` section in https://www.freedesktop.org/software/systemd/man/systemd.service.html for details)
```
[Unit]
...

[Install]
...

[Service]
...
...
Restart=always
RestartSec=30
...
```
#### Timers
* :bulb: **much** better description and examples: https://blogs.reliablepenguin.com/2025/10/15/systemd-timers-a-practical-guide-to-replacing-cron-on-linux
* https://wiki.archlinux.org/index.php/Systemd/Timers

```shell
# List all timers
systemctl list-timers
# List all timers (including inactive)
systemctl list-timers --all
```

#### Auto-mounting
* https://sleeplessbeastie.eu/2017/09/25/how-to-mount-webdav-share-using-systemd/
* https://unix.stackexchange.com/questions/283442/systemd-mount-fails-where-setting-doesnt-match-unit-name/345518#345518

```shell
# Mounting fails when mountpoint contains dash 
# mnt-seafile-user.automount: Where= setting doesn't match unit name. Refusing.

# Using underscore would have solved the problem according to systemd-escape:
# The following command outputs "mnt-seafile_user.automount"
systemd-escape -p --suffix=automount "/mnt/seafile_user"
# But it doesn't. At least on Ubuntu 18.04 (bionic) using "mnt_seafile_user.automount" as
# a unit name still fails
# [!!] TODO: test on more recent versions of Ubuntu
# So we keep dash and use ugly escaping "mnt-seafile\x2duser.automount"
```

```shell
[!] Note the double backslash
nano /etc/systemd/system/mnt-seafile\\x2user.mount
```
```
[Unit]
Description=Mount user datastore on host.domain.tld
After=network-online.target
Wants=network-online.target

[Mount]
What=https://host.domain.tld:1234/seafdav
Where=/mnt/seafile-user
Options=noauto,user,uid=user,gid=user,_netdev
Type=davfs
TimeoutSec=60

[Install]
WantedBy=remote-fs.target
```
```shell
[!] Note the double backslash again
nano /etc/systemd/system/mnt-seafile\\x2user.automount
```
```
[Unit]
Description=Auto-mount user datastore on host.domain.tld
After=network-online.target
Wants=network-online.target

[Automount]
Where=/mnt/seafile-user
TimeoutIdleSec=300

[Install]
WantedBy=remote-fs.target
```
```shell
systemctl daemon-reload
systemctl status mnt-seafile\\x2duser.automount
systemctl is-enabled mnt-seafile\\x2duser.automount
systemctl enable mnt-seafile\\x2duser.automount
systemctl start mnt-seafile\\x2duser.automount
```

#### Override some settings in existing unit file

* :point_right: https://askubuntu.com/questions/659267/how-do-i-override-or-configure-systemd-services/659268#659268

The correct way to do this is to create a directory named after the unit file with `.d` appended on the end. So for a unit called `example.service`, a subdirectory called `example.service.d` could be created. Within this directory a file ending with `.conf` can be used to override or extend the attributes of the system's unit file.

For example, for a unit file `/run/systemd/generator.late/isc-dhcp-server.service` (automatically generated for `/etc/init.d/isc-dhcp-server`) the drop-in file name will be:<br>
`/etc/systemd/system/isc-dhcp-server.service.d/enable-autorestart.conf`<br>
:warning: Don't forget to copy section name
```shell
# or use edit command to create drop-in file override.conf automatically
systemctl edit apt-cacher-ng.service

# [!!] Timer unit example
systemctl edit dnf-automatic-install.timer
```
:warning: Explicitly clear ExecStart before setting it again, as it is an additive setting, similar to other lists like `Environment` (as a whole, not per-variable) and `EnvironmentFile`. Otherwise you will get the error "bluetooth.service: Service has more than one ExecStart= setting, which is only allowed for Type=oneshot services. Refusing."
```
[Service]
ExecStart=
ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=avrcp
```

To check if the file is in use view service status:
```
# systemctl status isc-dhcp-server.service
● isc-dhcp-server.service - LSB: DHCP server
   Loaded: loaded (/etc/init.d/isc-dhcp-server; generated; vendor preset: enabled)
  Drop-In: /etc/systemd/system/isc-dhcp-server.service.d
           └─enable-autorestart.conf
```
* https://freedesktop.org/software/systemd/man/systemd.service.html
* https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files

#### Sample simple service unit file
```
[Unit]
Description=My Miscellaneous Service
After=network.target

[Service]
# Another Type option: forking
Type=simple
User=username
WorkingDirectory=/home/username
ExecStart=/home/username/my_daemon --option=123
# Other Restart options: on-failure, on-abort, etc.
Restart=always

[Install]
WantedBy=multi-user.target
```
* Where to put systemd unit file
    * The best place to put system unit files: `/etc/systemd/system`
    * The best place to put user unit files: `/etc/systemd/user` or `$HOME/.config/systemd/user`, but it depends on permissions and the situation
        * :warning: **2check**: multiple *per-user* instances of a service?
        * https://superuser.com/questions/853717/what-is-the-difference-between-systemds-user-and-system-services/860598#860598
    * https://unix.stackexchange.com/questions/224992/where-do-i-put-my-systemd-unit-file/367237#367237

Unit file registration
```shell
nano /etc/systemd/system/myservice.service
systemctl daemon-reload
systemctl enable myservice.service
```
