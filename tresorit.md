```shell
.local/share/tresorit/tresorit-cli status
.local/share/tresorit/tresorit-cli sync --start tresor-name --path /path/to/tresors/tresor-name
```

```
[Unit]
Description=Tresorit daemon example
After=network.target

[Service]
Type=forking
User=vagrant
WorkingDirectory=/home/vagrant
ExecStart=/home/vagrant/.local/share/tresorit/tresorit-cli start
ExecStop=/home/vagrant/.local/share/tresorit/tresorit-cli stop
# Other Restart options: on-failure, on-abort, etc.
Restart=always
PIDFile=/home/vagrant/.local/share/tresorit/tresorit-daemon.lock

[Install]
WantedBy=multi-user.target
```
