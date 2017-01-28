* https://liquidstate.net/how-to-manage-your-crashplan-server-remotely/

```shell
# <serviceHost>localhost</serviceHost> ==> <serviceHost>0.0.0.0</serviceHost> 
gedit /usr/local/crashplan/conf/my.service.xml
/usr/local/crashplan/bin/CrashPlanEngine status|start|stop|restart
```
