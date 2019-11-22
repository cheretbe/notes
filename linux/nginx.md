```
server_name _;
```

Safe restart: [safely_restart_nginx.sh](../files/nginx/safely_restart_nginx.sh)

```shell
ln -s /etc/nginx/sites-available/www.example.org.conf /etc/nginx/sites-enabled/
service nginx configtest
# If test fails review log
tail -f /var/log/nginx/error.log
service nginx force-reload
```
* https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
* https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04
* https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7
* https://www.nginx.com/resources/admin-guide/serving-static-content/

### Server blocks
* https://nginx.org/en/docs/http/request_processing.html
* https://nginx.org/en/docs/http/ngx_http_core_module.html#listen
* https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-16-04

### PHP
```
apt install php-fpm
service php7.2-fpm status
```

### SSL
http -> https redirection
```
server {
    listen       80 default_server;
    server_name  _;

    location / {
        return 301 https://$host$request_uri;
    }
}
```

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

* **https://www.daveperrett.com/articles/2009/08/10/passing-ips-to-apache-with-nginx-proxy/** (test with nextcloud/owncloud)
* https://philio.me/showing-the-correct-client-ip-in-logs-and-scripts-when-using-nginx-behind-a-reverse-proxy/
* Setup:
    * https://www.techandme.se/set-up-nginx-reverse-proxy/
    * https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-16-04-server
    * https://www.howtoforge.com/tutorial/how-to-install-nginx-as-reverse-proxy-for-apache-on-ubuntu-16-04/
    * https://www.techandme.se/set-up-nginx-reverse-proxy/
    * https://forum.nginx.org/read.php?2,234641,234641#msg-234641
    * https://www.ssltrust.com.au/blog/nginx-reverse-proxy-setup-guide/


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
```html
<!doctype html>
<html lang=en>
  <head>
    <meta charset=utf-8>
    <title>Test Page</title>
    <style>
      info-text {
        /* https://stackoverflow.com/questions/38781089/font-family-monospace-monospace */
        font-family: monospace, monospace;
      }
    </style>
  </head>
  <body>
    <info-text>
      <?php
        echo "HTTP_HOST: " . $_SERVER['HTTP_HOST'] . "<br>";
        echo "REMOTE_ADDR: " . $_SERVER['REMOTE_ADDR'] . "<br>";
        echo "HTTP_X_REAL_IP: " . $_SERVER['HTTP_X_REAL_IP'] . "<br>";
        echo "HTTP_USER_AGENT: " . $_SERVER['HTTP_USER_AGENT'] . "<br>";
        echo "---------------------------------------------";
      ?>
    </info-text>
    <?php phpinfo(); ?>
  </body>
</html>
```
