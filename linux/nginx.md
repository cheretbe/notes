```shell
ln -s /etc/nginx/sites-available/www.example.org.conf /etc/nginx/sites-enabled/
service nginx configtest
# If test fails review log
tail -f /var/log/nginx/error.log
service nginx force-reload
```

* How To Install Nginx on Ubuntu 16.04: https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04
* How To Install Nginx on CentOS 7: https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7
* Serving static content: https://www.nginx.com/resources/admin-guide/serving-static-content/
* How To Set Up Nginx Server Blocks (Virtual Hosts) on Ubuntu 16.04: https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-16-04

### SSL
```shell
sudo mkdir /etc/nginx/ssl
cp domain.com.bundle.crt /etc/nginx/ssl
cp comain.com.key /etc/nginx/ssl
# Nginx starts off as root before spawning its individual worker processes
sudo chown -R root:root /etc/nginx/ssl
sudo chmod -R 600 /etc/nginx/ssl
```
config
```
server {
    listen 443 ssl;
    server_name www.domain.com;
    ssl on;

    ssl_certificate /etc/nginx/ssl/domain.com.bundle.crt;
    ssl_certificate_key /etc/nginx/ssl/domain.com.key;
    ...
}
```

### Reverse proxy

See [phpnuget setup](phpnuget.md) for nginx -> apache proxy example<br><br>

Get client's real IP when behind NAT or a proxy/load balancer
```
http {
  ...
  set_real_ip_from 192.168.1.1;
  set_real_ip_from 192.168.1.2;
  real_ip_header X-Forwarded-For;
  ...
}
```
Then use on server
```php
<? echo $_SERVER["REMOTE_ADDR"]; ?>
```
* https://philio.me/showing-the-correct-client-ip-in-logs-and-scripts-when-using-nginx-behind-a-reverse-proxy/

Setup:
* https://www.techandme.se/set-up-nginx-reverse-proxy/
* https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-16-04-server
* https://www.howtoforge.com/tutorial/how-to-install-nginx-as-reverse-proxy-for-apache-on-ubuntu-16-04/
* https://www.techandme.se/set-up-nginx-reverse-proxy/
* https://forum.nginx.org/read.php?2,234641,234641#msg-234641
* https://www.ssltrust.com.au/blog/nginx-reverse-proxy-setup-guide/
