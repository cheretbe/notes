https://docs.mitmproxy.org/stable/
https://docs.mitmproxy.org/stable/howto-transparent/

```shell
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1

# Disable ICMP redirects
# If your test device is on the same physical network, your machine
# shouldn’t inform the device that there’s a shorter route available
# by skipping the proxy
sysctl -w net.ipv4.conf.all.send_redirects=0

ip link

iptables -t nat -A PREROUTING -i enp0s8 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i enp0s8 -p tcp --dport 443 -j REDIRECT --to-port 8080

ip6tables -t nat -A PREROUTING -i enp0s8 -p tcp --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -i enp0s8 -p tcp --dport 443 -j REDIRECT --to-port 8080

pip install mitmproxy

# Note the address and change default route on client
ip addr

# run as ordinary user to simplify access to certificates in ~/.mitmproxy
# https://docs.mitmproxy.org/stable/concepts-options/
# [!!!] Use Shift key to select text with mouse (also to bring right-click context menu up)
mitmproxy --mode transparent --showhost --set console_focus_follow=true
```
