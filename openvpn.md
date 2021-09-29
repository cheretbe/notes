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
```shell
apt install openvpn openvpn-systemd-resolved
openvpn --config /vagrant/temp/nl2-ovpn-udp.ovpn --auth-user-pass /vagrant/temp/pwdfile
```

```
script-security 2
up /etc/openvpn/update-systemd-resolved
down /etc/openvpn/update-systemd-resolved
down-pre
```
