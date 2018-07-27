* DNS Benchmark: https://www.grc.com/dns/benchmark.htm

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
# Status and stats
rndc status
rndc stats
less /var/cache/bind/named.stats

# View cache (dumped to /var/cache/bind/named_dump.db)
rndc dumpdb -cache
less /var/cache/bind/named_dump.db
grep facebook.com /var/cache/bind/named_dump.db

# Flush cache
rndc flush
# Reload bind9
rndc reload

# The dump file should be empty if there were no DNS queries after flushing
rndc stats
less /var/cache/bind/named.stats
rndc dumpdb -cache
less /var/cache/bind/named_dump.db
```

```shell
dig yandex.ru @192.168.2.17 -p5353
nslookup -port=5353 yandex.ru 192.168.2.17
```

* https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-caching-or-forwarding-dns-server-on-ubuntu-14-04
* https://pujiermanto.wordpress.com/2017/06/14/how-to-view-and-clear-bind-dns-servers-cache-on-linux/
