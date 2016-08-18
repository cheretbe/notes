Change logging interval to 1 minute (weewx service has to be stopped):
```
wee_device --set-interval=1
```

```
# Last DB record
sqlite3 /var/lib/weewx/weewx.sdb 'select max(datetime(dateTime, "unixepoch", "localtime")), windSpeed, windGust from archive;'
# Last 10 records
sqlite3 /var/lib/weewx/weewx.sdb 'select datetime(dateTime, "unixepoch", "localtime") as dt, windSpeed, windGust from archive order by dt desc limit 10;'
```
