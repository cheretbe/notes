softlink: /opt/serviio -> serviio-1.8/

/lib/systemd/system/serviio.service
```
[Unit]
Description=Serviio Media Server
After=syslog.target local-fs.target network.target

[Service]
Type=simple
User=serviio
Group=serviio
ExecStart=/opt/serviio/bin/serviio.sh
ExecStop=/opt/serviio/bin/serviio.sh -stop
KillMode=none
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
/opt/serviio/plugins/playlist.groovy
