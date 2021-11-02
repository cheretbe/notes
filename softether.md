* https://www.softether.org/
* https://techlist.top/softether-vpn-ustanovka-iz-repozitoriev-ubuntu-18-04/
* https://ubuntu.com/server/docs/network-dhcp
* https://launchpad.net/~paskal-07/+archive/ubuntu/softethervpn

```shell

add-apt-repository ppa:paskal-07/softethervpn

apt install softether-vpnserver softether-vpncmd

systemctl status softether-vpnserver

vpncmd
```
Config is in `/usr/libexec/softether/vpnserver/vpn_server.config`<br>
Logs are in `/usr/libexec/softether/vpnserver/*_log`

### DHCP server
```shell
apt install isc-dhcp-server
cp /etc/dhcp/dhcpd.conf{,.bak}
nano /etc/dhcp/dhcpd.conf
```
`/etc/dhcp/dhcpd.conf`:
```
# 0.5 days
default-lease-time 43200;
# 1 day
max-lease-time 86400;
 
subnet 192.168.2.0 netmask 255.255.255.0 {
  range 192.168.2.10 192.168.2.100;
}

# Fixed address for a host
host my-host {
  hardware ethernet 00:00:00:00:00:00;
  fixed-address 192.168.2.101;
}
```

`/etc/default/isc-dhcp-server`:
```
INTERFACESv4="eth4"
```
```shell
# Apply changes
systemctl restart isc-dhcp-server.service
```

