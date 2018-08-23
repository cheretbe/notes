```shell
# View version
/usr/bin/SpiderOakONE --version

# Running in GUI mode with X11 forwarding via su
# [!] As the original user. Note the last line
xauth -f ~/.Xauthority list
# Switch user
sudo su - spideroak-user-name
xauth add host.domain.tld:10  MIT-MAGIC-COOKIE-1  75260434b52f448f9e21e0cf8c694102
/usr/bin/SpiderOakONE
# Shutting down (we don't have access to the tray icon)
<Ctrl>+Z
ps -aux | grep '/opt/SpiderOakONE/lib/SpiderOakONE'
# Note the PID of a process without --spider option
kill -KILL <pid>
```

```batch
:: View device numbers
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --user-info
```

### Permanent deletion

![exclamation](https://github.com/cheretbe/notes/blob/master/images/warning_16.png) **Quit SpiderOak ONE before deletion**

```batch
:: Device number is optional and defaults to the current device
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --device=2 --purge="C:\Documents and Settings\My Documents\unwanted.docx"
```
You can only delete data on a different device if you are using the same operating system.
For example, while seated at a Mac you cannot delete files that had been uploaded from device running Windows

Purge deleted items **older than** N days

```batch
"C:\Program Files\SpiderOakONE\SpiderOakONE.exe" --verbose --purge-deleted-items=PURGE_DAYS
```

* https://support.spideroak.com/hc/en-us/articles/115001891343-Command-Line-Reference
* https://support.spideroak.com/hc/en-us/articles/115001932006--purge
