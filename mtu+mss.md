* wireguard + python script examples
   *  https://github.com/nitred/nr-wg-mtu-finder
   *  https://gist.github.com/nitred/f16850ca48c48c79bf422e90ee5b9d95
   *  https://skym.fi/blog/2021/08/the-fun-called-mtu-and-wireguard/
   *  https://keremerkan.net/posts/wireguard-mtu-fixes/

```shell
# Due to the IP+ICMP packet overhead, the packet size is equal to the data size + 28 bytes. For example, if
# testing shows that only pings with size 1444 can pass normally, the MTU should be set to 1444+28 = 1472
# 1472(1500)
# -M pmtudisc_opt Select Path MTU Discovery strategy - do (prohibit fragmentation, even local one)
# [!!!] Don't try to guest the MTU, just set highest available value and then view cached record
ping -c 1 host -M do -s 1472
# View cached MTU
ip route get 8.8.8.8
# all cached records
ip route show cache
# flush cache
ip route flush cache

# Mikrotik
/ping count=1 host do-not-fragment size=1500
# Windows
ping -n 1 -f -l 1472 host
netsh interface ipv4 show destinationcache
netsh interface ipv4 show destinationcache address=8.8.8.8
netsh interface ipv4 delete destinationcache

# Check for ICMP type 3 code 4 message
# -p          Don't put the interface into promiscuous mode.
# -s snaplen  Snarf snaplen bytes of data from each packet rather than the default of 262144 bytes
tcpdump -s0 -p -ni eth0 'icmp and icmp[0] == 3 and icmp[1] == 4'

# Test download
# -p,  --page-requisites    get all images, etc. needed to display HTML page.
wget -p URL -O /dev/null
```
* :warning: **https://habr.com/ru/post/136871/**
* :warning: **https://forums.clavister.com/viewtopic.php?t=11915**
* **https://jamesdobson.name/post/mtu/**
* **https://toster.ru/q/502322**
* **https://support.ispsupplies.com/hc/en-us/articles/115009659067-PMTU-and-MSS-Discovery-Issues-Resolved-with-MikroTik**
* https://www.cellstream.com/reference-reading/tipsandtricks/407-ipv6-path-mtu-discovery-demystified
* http://www.oznetnerd.com/mtu-vs-mss-part-two/
* https://help.keenetic.com/hc/ru/articles/214470885-%D0%9A%D0%B0%D0%BA-%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B8%D1%82%D1%8C-%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80-MTU-
-----


* https://www.cisco.com/c/en/us/support/docs/ip/generic-routing-encapsulation-gre/25885-pmtud-ipfrag.html

There are three things that can break PMTUD, two of which are uncommon and one of which is common.

*   A router can drop a packet and not send an ICMP message. (Uncommon)
*   A router can generate and send an ICMP message, but the ICMP message gets blocked by a router or firewall between this router and the sender. (Common)
*   A router can generate and send an ICMP message, but the sender ignores the message. (Uncommon)

The first and last of the three bullets here are uncommon and are usually the result of an error, but the middle bullet describes a common problem. People that implement ICMP packet filters tend to block all ICMP message types rather than only blocking certain ICMP message types. A packet filter can block all ICMP message types except those that are "unreachable" or "time-exceeded." The success or failure of PMTUD hinges upon ICMP unreachable messages getting through to the sender of a TCP/IPv4 packet. ICMP time-exceeded messages are important for other IPv4 issues. An example of such a packet filter, implemented on a router is shown here.

```
> <pre>access-list 101 permit icmp any any unreachable
> access-list 101 permit icmp any any time-exceeded
> access-list 101 deny icmp any any
> access-list 101 permit ip any any</pre>
```

There are other techniques that can be used in order to help alleviate the problem of ICMP being completely blocked.

* http://packetlife.net/blog/2008/aug/18/path-mtu-discovery/

```
tracepath -n 192.168.1.2
```
On Windows try https://elifulkerson.com/projects/mturoute.php
