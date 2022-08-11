* https://yandex.ru/support/disk/cli-clients.html

```shell
yandex-disk setup
```

`/etc/supervisor/conf.d/yandex-disk.conf`
```
[program:yandex-disk]
command=/usr/bin/yandex-disk --dir=/path/to/yandex-disk --no-daemon
user=username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile = /var/log/supervisor/yandex-disk.log
```

```
Synchronization core status: no internet access
Synchronization core status: index
Synchronization core status: idle
```
