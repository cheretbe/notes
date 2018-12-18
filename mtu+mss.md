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
