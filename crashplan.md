* https://liquidstate.net/how-to-manage-your-crashplan-server-remotely/

```
Important directories:
  Installation:
    /usr/local/crashplan
  Logs:
    /usr/local/crashplan/log
  Default archive location:
    /usr/local/var/crashplan
  Readme:
    /usr/local/crashplan/doc

Start Scripts:
  sudo /usr/local/crashplan/bin/CrashPlanEngine start|stop
  /usr/local/crashplan/bin/CrashPlanDesktop
```

```shell
# <serviceHost>localhost</serviceHost> ==> <serviceHost>0.0.0.0</serviceHost> 
gedit /usr/local/crashplan/conf/my.service.xml
/usr/local/crashplan/bin/CrashPlanEngine status|start|stop|restart
```
