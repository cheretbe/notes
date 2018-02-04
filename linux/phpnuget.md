* http://www.kendar.org/?p=/dotnet/phpnuget
* https://www.cnblogs.com/ljzforever/p/6241490.html

```
apt install zip apache2 libapache2-mod-php php-curl php-zip php-xml
a2enmod rewrite
```
Debian jessie: `zip apache2 libapache2-mod-php5 php5-curl php-pclzip php-xml-parser`

Change port in `/etc/apache2/ports.conf` ~~and `/etc/apache2/sites-available/000-default.conf`, enable `php_curl` in `/etc/php/7.0/apache2/php.ini`~~

```shell
a2dissite 000-default
```

Create `/etc/apache2/sites-available/phpnuget.conf` with the following content
```apache
<VirtualHost *:8080>
  ServerName host.domain.tld
  ServerAlias host1.domain.tld
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

wget http://www.kendar.org/?p=/dotnet/phpnuget/phpnuget.zip -O phpnuget.zip
unzip phpnuget.zip
cp -R src/ /www/phpnuget
chown www-data /www/phpnuget/
chown www-data /www/phpnuget/data/ -R
chown www-data /www/phpnuget/settings.php
chown www-data /www/phpnuget/.htaccess
```

Got to `http://host/phpnuget/setup.php` and finish setup

```
# remove write permissions
chown root /www/phpnuget/
chown root /www/phpnuget/settings.php
chown root /www/phpnuget/.htaccess
```

nginx reverse proxy
```
  location /phpnuget {
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  X-Forwarded-For $remote_addr;
    proxy_set_header  Host $host;
    proxy_pass        http://localhost:8080/phpnuget;
  }
```

```batch
:: Publish
choco install Nuget.CommandLine
nuget push package.nupkg Token -src http://host/phpnuget/upload

:: Use on client
choco source add -n=test -s=http://host/phpnuget/api/v2/
choco install package
```
