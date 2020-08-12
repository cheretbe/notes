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
DHCP server
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
```

`/etc/default/isc-dhcp-server`:
```
INTERFACESv4="eth4"
```

