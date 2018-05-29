* http://www.kendar.org/?p=/dotnet/phpnuget
* https://www.cnblogs.com/ljzforever/p/6241490.html
* https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-16-04-server
* https://devops.profitbricks.com/tutorials/configure-nginx-as-a-reverse-proxy-for-apache-on-ubuntu-1604/

```
apt install zip apache2 libapache2-mod-php php-curl php-zip php-xml
a2enmod rewrite
```
Debian jessie: `zip apache2 libapache2-mod-php5 php5-curl php-pclzip php-xml-parser`

Change port in `/etc/apache2/ports.conf` ~~and `/etc/apache2/sites-available/000-default.conf`, enable `php_curl` in `/etc/php/7.0/apache2/php.ini`~~

```shell
a2dissite 000-default
```
For apache to be able to correctly resolve client IPs from behind a proxy `mod_rpaf` is needed.
```shell
# [!] libapache2-mod-rpaf package in Debian/Ubuntu is outdated and doensn't support RPAF_SetHTTPS option
# We will use a fork instead. Node syntax difference, e.g. RPAF_ProxyIPs instead of RPAFproxy_ips, etc.
mkdir -p ~/sources
cd ~/sources
wget https://github.com/gnif/mod_rpaf/archive/stable.zip
unzip stable.zip
cd mod_rpaf-stable
make
sudo make install
```
Create `/etc/apache2/mods-available/rpaf.load` file with the following content:
```
LoadModule rpaf_module /usr/lib/apache2/modules/mod_rpaf.so
```
Create `/etc/apache2/mods-available/rpaf.conf` file with the following content:
```
<IfModule mod_rpaf.c>
    RPAF_Enable             On
    RPAF_Header             X-Real-Ip
    RPAF_ProxyIPs           your_server_ip 
    RPAF_SetHostName        On
    RPAF_SetHTTPS           On
    RPAF_SetPort            On
</IfModule>
```
```shell
# Enable module
a2enmod rpaf
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
