* https://github.com/juanfont/headscale
    * https://tailscale.com/kb/1151/what-is-tailscale/
    * https://vc.ru/dev/497249-razvorachivaem-tailscale-vpn-u-sebya-v-oblake

```shell
# WG server
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -A FORWARD -i wg0 -o wg0 -j ACCEPT

# LAN router
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --table nat --append POSTROUTING -s 192.168.101.0/24 --out-interface wg-hub -j MASQUERADE
```
