Change logging interval to 1 minute (weewx service has to be stopped):
```
wee_device --set-interval=1
# View current setting (here it is called "read_period")
wee_device --info
wee_device --info | grep read_period
```

Post interval (post_interval).
```
[StdRestful]
    [[WindGuru]]
        password = xxx
        station_id = yyy
        post_interval = 60
```
Actually it's more of a "Not To Exceed" interval:
https://groups.google.com/d/msg/weewx-user/Ot4O3Yu4rwg/8vAuQa5bEAAJ

DB queries
```
# Last DB record
sqlite3 /var/lib/weewx/weewx.sdb 'select max(datetime(dateTime, "unixepoch", "localtime")), windSpeed, windGust from archive;'
# Last 10 records
sqlite3 /var/lib/weewx/weewx.sdb 'select datetime(dateTime, "unixepoch", "localtime") as dt, windSpeed, windGust from archive order by dt desc limit 10;'
```
