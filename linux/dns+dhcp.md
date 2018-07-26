```shell
apt install bind9 bind9utils bind9-doc
```

Just disabling bind to listen on IPv6 addresses does not prevents it from querying for
IPv6 addresses to remote hosts. To ensure that IPv6 is completely disabled use:
```
filter-aaaa-on-v4 yes;

// Listen on custom port (IPv4)
listen-on port 5353 {any;};
// Listen on one interface only
listen-on port 53 {192.168.2.17;};
```

```shell
dig yandex.ru @192.168.2.17 -p5353
nslookup -port=5353 yandex.ru 192.168.2.17
```

* https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-caching-or-forwarding-dns-server-on-ubuntu-14-04
