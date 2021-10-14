* Exclude specific file types from sync (advanced): https://support.tresorit.com/hc/en-us/articles/217103697-Exclude-specific-file-types-from-sync-advanced-

```shell
.local/share/tresorit/tresorit-cli status
.local/share/tresorit/tresorit-cli login --email user@domain.tld --password-on-stdin
.local/share/tresorit/tresorit-cli sync --start tresor-name --path /path/to/tresors/tresor-name
.local/share/tresorit/tresorit-cli transfers
.local/share/tresorit/tresorit-cli transfers --files
.local/share/tresorit/tresorit-cli transfers --files --tresor tresor-name
```

```shell
nano /etc/systemd/system/tresorit.service
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

```shell
systemctl daemon-reload
systemctl enable tresorit.service
```
