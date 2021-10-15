* https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/

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

#### DNS
DNS management for VPNs with `systemd-resolved` is a mess:
* https://github.com/systemd/systemd/issues/6076
* https://askubuntu.com/questions/1032476/ubuntu-18-04-no-dns-resolution-when-connected-to-openvpn/1036209#1036209
* `openvpn-systemd-resolved` package installs a copy of https://github.com/jonathanio/update-systemd-resolved as `/etc/openvpn/update-systemd-resolved`
    * `update-systemd-resolved` **adds** VPN DNS servers to server(s) already received by DHCP, not replaces them
* [Linux app from PureVPN](https://www.purevpn.com/download/linux-vpn) uses `/etc/purevpn/pure-resolv-conf` script to overwrite `/etc/purevpn/dns.conf` (or a link source) and restores it on disconnect
* https://github.com/cheretbe/vagrant-files/blob/develop/windows/win10-vpn-local/provision/update_resolve_conf.py

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
