* http://www.kendar.org/?p=/dotnet/phpnuget
* https://www.cnblogs.com/ljzforever/p/6241490.html

```
apt install zip apache2 libapache2-mod-php php-curl php-zip php-xml
a2enmod rewrite
```
Change port in `/etc/apache2/ports.conf` ~~and `/etc/apache2/sites-available/000-default.conf`~~, enable `php_curl` in `/etc/php/7.0/apache2/php.ini`

```shell
a2dissite 000-default
```

Create `/etc/apache2/sites-available/phpnuget.conf` with the following content
```apache
<VirtualHost *:8080>
  Alias /phpnuget "/www/phpnuget"
  <Directory "/www/phpnuget">
    AllowOverride All
    Require all granted
  </Directory>

  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

```
a2ensite phpnuget
```

nginx reverse proxy
```
  location /phpnuget {
    proxy_pass              http://localhost:8080/phpnuget;
  }
```
