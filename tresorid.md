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
# Other Restart options: always, on-abort, etc.
Restart=on-failure
PIDFile=/home/vagrant/.local/share/tresorit/tresorit-daemon.lock

[Install]
WantedBy=multi-user.target
```
