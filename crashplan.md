* https://liquidstate.net/how-to-manage-your-crashplan-server-remotely/
* https://support.code42.com/CrashPlan/4/Configuring/Using_CrashPlan_On_A_Headless_Computer


Uninstallation
* https://support.code42.com/CrashPlan/4/Troubleshooting/Uninstalling_And_Reinstalling_The_Code42_CrashPlan_App

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

Copy the authentication token from the `/var/lib/crashplan/.ui_info` file from the remote computer to the local computer. On local computer:
```
sudo su -
cp /var/lib/crashplan/.ui_info{,.bak}
nano /var/lib/crashplan/.ui_info
```
Windows: `C:\ProgramData\CrashPlan\.ui_info`

![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) Local Crashplan service **overwrites** this file on **every start**
