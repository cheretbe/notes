```shell
# Find system boot-up performance statistics
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
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

Auto-start service after crash
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
To check if the file is in use view service status:
```
# systemctl status isc-dhcp-server.service
● isc-dhcp-server.service - LSB: DHCP server
   Loaded: loaded (/etc/init.d/isc-dhcp-server; generated; vendor preset: enabled)
  Drop-In: /etc/systemd/system/isc-dhcp-server.service.d
           └─enable-autorestart.conf
```
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
# Other Restart options: always, on-abort, etc.
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Unit file registration
```shell
nano /etc/systemd/system/myservice.service
systemctl daemon-reload
systemctl enable myservice.service
```
