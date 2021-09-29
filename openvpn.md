### Windows

TAP adapter to try on Windows 7 with driver signature problems: https://build.openvpn.net/downloads/releases/tap-windows-9.21.2.exe

```bat
:: List TAP adapters
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" hwids tap*

:: Remove adapter
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" remove tap0901

:: Create adapter
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" install "C:\Program Files\TAP-Windows\driver\OemVista.inf" tap0901


"C:\Program Files\OpenVPN\bin\openvpn.exe" --show-adapters
"C:\Program Files\OpenVPN\bin\openvpn.exe" --show-net
```

### Linux

* https://askubuntu.com/questions/1032476/ubuntu-18-04-no-dns-resolution-when-connected-to-openvpn/1036209#1036209
* 
```shell
apt install openvpn openvpn-systemd-resolved
openvpn --config /vagrant/temp/nl2-ovpn-udp.ovpn --auth-user-pass /vagrant/temp/pwdfile
```

```
script-security 2
up /etc/openvpn/update-systemd-resolved
; Enable the --up and --down scripts to be called for restarts as well as initial program start.
up-restart
down /etc/openvpn/update-systemd-resolved
; Call --down cmd/script before, rather than after, TUN/TAP close.
down-pre
```
