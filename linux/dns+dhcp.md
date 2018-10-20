* https://blogging.dragon.org.uk/dns-bind9-dhcp-ubuntu-16-04-2/
* DNS Benchmark: https://www.grc.com/dns/benchmark.htm
    * Build Custom Nameserver List: System menu (Alt+Space) --> Build Custom Nameserver List
    
:exclamation: `apt-get remove avahi-daemon`
```
# -n     Don't convert addresses (i.e., host addresses, port numbers, etc.) to names
tcpdump -n -i enp0s9 port bootps or port bootpc
```
    
#### Bind9 installation and initial setup

```shell
# Install packages
apt install bind9 bind9utils bind9-doc
# Backup default configuration
cp /etc/bind/named.conf.options{,.bak}
cp /etc/bind/named.conf.local{,.bak}
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

// https://lists.isc.org/pipermail/bind-users/2015-September/095748.html
no-case-compress { 10.0.0.0/8; };
```

Zones information is in `/etc/bind/named.conf.local`
```
zone "domain.tld" {
	type master;
	file "/etc/bind/zones/domain.tld.zone";
	allow-update { key rndc-key; };
};

zone "2.168.192.in-addr.arpa" {
     type master;
     file "/etc/bind/zones/192.168.2.rev.zone";
     allow-update { key rndc-key; };
};
```

```shell
# Directory for zone files
mkdir -p /etc/bind/zones
# /etc/bind should have setGID bit set and therefore should inherit group "bind" for
# newly created directory. Make sure group has write access to it so that bind could
# create .jnl files in process of updating dynamic records
chmod g+w /etc/bind/zones
```
`$ORIGIN` defines a base name from which "unqualified" names (those without a terminating dot) substitutions are made when processing the zone file. If an `$ORIGIN` directive is not defined BIND generates it automatically from the zone name.<br>
:warning: **Note trailing full stops**

`/etc/bind/zones/domain.tld.zone`
```
$ORIGIN domain.tld.
$TTL 1h         ; default expiration time of all resource records without their own TTL value
@                IN SOA	ns1.domain.tld. admin.domain.tld. (
				2018073001 ; serial
				86400      ; refresh (24 hours)
				7200       ; retry (2 hours)
				604800     ; expire (1 week)
				600        ; minimum (10 minutes)
				)
			NS	ns1
 
router			A	192.168.2.1
ns1			A	192.168.2.3
dns-dhcp		CNAME	ns1          ; the name of the server we are building
```
`/etc/bind/zones/192.168.2.rev.zone`
```
$TTL 1h         ; default expiration time of all resource records without their own TTL value
@                IN SOA	ns1.domain.tld. admin.domain.tld. (
				2018073001 ; serial
				86400      ; refresh (24 hours)
				7200       ; retry (2 hours)
				604800     ; expire (1 week)
				600        ; minimum (10 minutes)
				)
			NS	ns1.domain.tld.

1			PTR	router.domain.tld.
3			PTR	dns-dhcp.domain.tld.
			PTR	domain.tld.
```
```shell
# Make sure DHCP server can update zone files
chown bind:bind /etc/bind/zones/*zone
chmod 664 /etc/bind/zones/*zone
```

```shell
# Check config, zones and restart service
named-checkconf
named-checkzone domain.tld /etc/bind/zones/domain.tld.zone
named-checkzone 2.168.192.in-addr.arpa /etc/bind/zones/192.168.2.rev.zone
service bind9 restart

# Make sure that DNS lookups (including reverse ones) work
dig router.domain.tld @192.168.2.3
dig -x 192.168.2.1 @192.168.2.3

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

#### Maintenance

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
# Flush the cache for a specific name as well as all records below that name
rndc flushtree domain.tld
# Reload bind9 (not needed)
# rndc reload

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

#### ISC DHCP server
```shell
# Install packages
apt install isc-dhcp-server
# Backup default configuration
cp /etc/default/isc-dhcp-server{,.bak}
cp /etc/dhcp/dhcpd.conf{,.bak}
```
If server has more than one NIC, make sure to update INTERFACESv4 (INTERFACESv6) parameters
in `/etc/default/isc-dhcp-server`

```shell
# Add service unit drop-in to override restart option
cat << EOF > /etc/systemd/system/isc-dhcp-server.service.d/enable-autorestart.conf
[Service]
Restart=always
RestartSec=30
EOF
# Apply settings
systemctl daemon-reload
```

```shell
# Use a copy of the key file (to preserve original file permissions)
cp /etc/bind/rndc.key /etc/dhcp/ddns-keys
chown root:root /etc/dhcp/ddns-keys/rndc.key
chmod 640 /etc/dhcp/ddns-keys/rndc.key
```

`/etc/dhcp/dhcpd.conf`
```
ddns-updates on;
ddns-update-style standard;
authoritative;

include "/etc/dhcp/ddns-keys/rndc.key";

default-lease-time 604800; # 7 days
max-lease-time 604800;

allow unknown-clients;
use-host-decl-names on;

zone domain.tld. {
  primary 192.168.2.3;  # This server is the primary DNS server for the zone
  key rndc-key;         # Use the key we defined earlier for dynamic updates
}
zone 2.168.192.in-addr.arpa. {
  primary 192.168.2.3;  # This server is the primary reverse DNS for the zone
  key rndc-key;         # Use the key we defined earlier for dynamic updates
}

subnet 192.168.20.0 netmask 255.255.255.0 {
  range 192.168.2.100 192.168.2.154;
  option subnet-mask 255.255.255.0;
  option routers 192.168.2.1;
  option domain-name-servers 192.168.2.3;
  option domain-name "domain.tld";
  ddns-domainname "domain.tld.";
  ddns-rev-domainname "in-addr.arpa.";
}
```

Execute script on commit
```
on commit {
    if (static) {
        set isst = "static";
    } else {
        set isst = "dynamic";
    }

    set clip = binary-to-ascii(10, 8, ".", leased-address);
    set clhw = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
    execute("/usr/local/sbin/dhcpevent", "commit", isst, clip, clhw, host-decl-name);}
```
* https://linux.die.net/man/5/dhcp-eval
* https://kb.isc.org/docs/aa-01039
* https://github.com/dploeger/dhcp-commit-report
* https://stackoverflow.com/questions/24052217/may-someone-explain-the-following-os-fork-example-to-me


```shell
# Check config without restarting service
# For custom path use -cf /custom/path/dhcpd.conf
dhcpd -t
# Restart service
service isc-dhcp-server restart
```

#### Maintenance
```shell
# Leases location
cat /var/lib/dhcp/dhcpd.leases
# Print active leases
dhcp-lease-list
# To get manufacturer names
wget -O /usr/local/etc/oui.txt http://standards-oui.ieee.org/oui/oui.txt

# Release a lease
service isc-dhcp-server stop
# Manually delete lease entry from the file
nano /var/lib/dhcp/dhcpd.leases
service isc-dhcp-server start
```

#### Pi-hole

`/etc/pihole/setupVars.conf`

#### systemd-resolved
```shell
systemd-resolve --status

```
Temporary fix for systemd-resolved not resolving `.local` names (both
`DNSStubListener=no` and updating `/etc/resolv.conf` link are needed):
* https://superuser.com/questions/1318220/ubuntu-18-04-disable-dnsmasq-base-and-enable-full-dnsmasq/1318279#1318279
* https://stackoverflow.com/questions/50299241/ubuntu-18-04-server-how-to-check-dns-ip-server-setting-being-used/51060649#51060649

#### DHCP client

See [notes](./networking.md#dhcp) in network settings

* https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-caching-or-forwarding-dns-server-on-ubuntu-14-04
* https://pujiermanto.wordpress.com/2017/06/14/how-to-view-and-clear-bind-dns-servers-cache-on-linux/
