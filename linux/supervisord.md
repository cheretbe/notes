* http://mneilsworld.com/discussion/supervisord-docker-and-loggly

Config files location: `/etc/supervisor/conf.d/`

```shell
# service is not enabled by default
sudo systemctl enable supervisor.service
sudo service supervisor start
# start/stop only one service
sudo supervisorctl stop service_name
sudo supervisorctl start service_name
# re-read config and restart changed services
sudo supervisorctl reread
sudo supervisorctl update
```

`/etc/supervisor/conf.d/dummy.conf`
```apache
[program:dummy]
command=/path/to/an/executable
user=username
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/dummy.log
redirect_stderr=true

# Uncomment if redirect_stderr is false
#stderr_logfile=/var/log/supervisor/dummy_err.log

# [!] logfile_maxbytes and logfile_backups are for [supervisord]
# section of /etc/supervisor/supervisord.conf file
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=3
```

Command with shell pipe redirection
```apache
command=/bin/bash -c "2>&1 /path/to/a/script.sh | /path/to/a/receiver_script.py"
# Needed to correctly stop child processes
stopasgroup=true
```

Dummy test bash "service" script
```shell
#!/bin/bash

while true
do
  echo "stdout test"
  sleep 3
  >&2 echo "stderr test"
  sleep 3
done
```
