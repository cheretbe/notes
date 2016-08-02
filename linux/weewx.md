```
sqlite3 /var/lib/weewx/weewx.sdb 'select max(datetime(dateTime, "unixepoch", "localtime")), windSpeed, windGust from archive;'
```
