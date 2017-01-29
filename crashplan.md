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

* https://support.code42.com/CrashPlan/4/Troubleshooting/Linux_Real-Time_File_Watching_Errors
```shell
# /etc/sysctl.conf
# fs.inotify.max_user_watches=1048576
sudo sysctl -p /etc/sysctl.conf
```
