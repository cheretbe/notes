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
...
```
