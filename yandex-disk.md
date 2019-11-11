* https://yandex.ru/support/disk/cli-clients.html

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
