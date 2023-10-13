* https://github.com/juanfont/headscale
    * https://tailscale.com/kb/1151/what-is-tailscale/
    * https://vc.ru/dev/497249-razvorachivaem-tailscale-vpn-u-sebya-v-oblake

### Unsorted

```shell
# WG server
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -A FORWARD -i wg0 -o wg0 -j ACCEPT

# LAN router
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --table nat --append POSTROUTING -s 192.168.101.0/24 --out-interface wg-hub -j MASQUERADE
```

Routing table example (for PBR)
```
[Interface]
Table = 42

[Peer]
# wg-quick will generate routes from all peers' AllowedIPs
Endpoint = <your_server>
AllowedIPs = 0.0.0.0/0, ::/0
```
* https://superuser.com/questions/1762082/address-based-routing-policy-for-linux-router

### Installation

```shell
apt install wireguard

cat > /etc/wireguard/wg0.conf<< EOF
[Interface]
Address = 10.1.1.0/24
ListenPort = 50800
PrivateKey = replace with wg genkey output
MTU = 1500
PostUp = 
PostDown =
EOF
```
