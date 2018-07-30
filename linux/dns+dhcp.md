* DNS Benchmark: https://www.grc.com/dns/benchmark.htm
    * Build Custom Nameserver List: System menu (Alt+Space) --> Build Custom Nameserver List
    
#### Bind9 installation and initial setup

```shell
# Install packages
apt install bind9 bind9utils bind9-doc
# Generate rndc authentication key
/usr/sbin/rndc-confgen -a -b 512
```
Generated `/etc/bind/rndc.key` should have `bind:bind(640)` ownership and permissions

Config is in `/etc/bind/named.conf.options`:
```
include "/etc/bind/rndc.key";

acl internals {
	127.0.0.1;
	192.168.2.0/24;
};

options {
	directory "/var/cache/bind";

	// dnssec-validation auto;
	dnssec-enable yes;
	dnssec-validation yes;

	auth-nxdomain no;    # conform to RFC1035
	listen-on-v6 { none; };
	// Just disabling bind to listen on IPv6 addresses does not prevents it from querying for
	// IPv6 addresses to remote hosts. To ensure that IPv6 is completely disabled use:
	filter-aaaa-on-v4 yes;

	listen-on port 5353 {any;};

	allow-query {
		internals;
	};
	allow-query-cache {
		internals;
	};
	recursion yes;
	allow-recursion {
		internals;
	};
	allow-transfer {
		internals;
	};
};
```

Additional options
```
listen-on-v6 { none; };
// Just disabling bind to listen on IPv6 addresses does not prevents it from querying for
// IPv6 addresses to remote hosts. To ensure that IPv6 is completely disabled use:
filter-aaaa-on-v4 yes;

// Listen on custom port (IPv4)
listen-on port 5353 {any;};
// Listen on one interface only
listen-on port 53 {192.168.2.17;};
```

Zones information is in `/etc/bind/named.conf.local`

```shell
# Check config and restart service
named-checkconf
service bind9 restart
```

#### SOA record
Examples
```
example.com.  3600  SOA  dns.example.com. hostmaster.example.com. (
                         1999022301   ; serial YYYYMMDDnn
                         86400        ; refresh (  24 hours)
                         7200         ; retry   (   2 hours)
                         3600000      ; expire  (1000 hours)
                         172800 )     ; minimum (   2 days)
```
```
google.com.		60 IN SOA ns1.google.com. dns-admin.google.com. (
				206526105  ; serial
				900        ; refresh (15 minutes)
				900        ; retry (15 minutes)
				1800       ; expire (30 minutes)
				60         ; minimum (1 minute)
				)
```
For a standalone server only serial number and minimum TTL are important
* https://www.ripe.net/publications/docs/ripe-203

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
# Non-standard port
dig yandex.ru @192.168.2.17 -p5353
# Doesn't work on Windows, use version from BIND package (https://www.isc.org/downloads/)
nslookup -port=5353 yandex.ru 192.168.2.17

# View SOA record
dig SOA +multiline domain.tld @192.168.2.17
nslookup -q=soa domain.tld
```

* https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-caching-or-forwarding-dns-server-on-ubuntu-14-04
* https://pujiermanto.wordpress.com/2017/06/14/how-to-view-and-clear-bind-dns-servers-cache-on-linux/
