```shell
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

**Override some settings in existing unit file**<br>
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
