* http://www.kendar.org/?p=/dotnet/phpnuget
* https://www.cnblogs.com/ljzforever/p/6241490.html

```
apt install zip apache2 libapache2-mod-php php-curl php-zip php-xml
a2enmod rewrite
```
Change port in `/etc/apache2/ports.conf` and `/etc/apache2/sites-available/000-default.conf`
Enable `php_curl` in `/etc/php/7.0/apache2/php.ini`

```apache
Alias /phpnuget "/www/phpnuget"
<Directory "/www/phpnuget">
  AllowOverride All
  Require all granted
</Directory>
```

nginx reverse proxy
```
  location /phpnuget {
    proxy_pass              http://localhost:8080/phpnuget;
  }
```
