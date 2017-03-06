* http://mneilsworld.com/discussion/supervisord-docker-and-loggly

Config files location: `/etc/supervisor/conf.d/`

```shell
# start/stop only one service
sudo supervisorctl stop service_name
sudo supervisorctl start service_name
# re-read config and restart changed services
sudo supervisorctl reread
sudo supervisorctl update
```
