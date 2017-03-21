* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-vnc-on-ubuntu-16-04

```
rm /tmp/.X1-lock
rm /tmp/.X11-unix/X1
vncserver -kill :1
```
