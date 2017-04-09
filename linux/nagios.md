```bash
apt install build-essential apache2 php apache2-mod-php7.0 php-gd libgd-dev sendmail unzip
# Set up the users and groups which Nagios expects
# These are in a few places in the default config; it’s not worth changing them
adduser nagios
addgroup nagcmd
usermod -a -G nagcmd nagios
usermod -a -G nagcmd www-data

cd temp
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.3.1.tar.gz
wget https://nagios-plugins.org/download/nagios-plugins-2.1.4.tar.gz
wget https://github.com/NagiosEnterprises/nrpe/archive/3.0.1.tar.gz
tar xzvf nagios-4.3.1.tar.gz
tar xzvf nagios-plugins-2.1.4.tar.gz
tar xzvf 3.0.1.tar.gz
```

* https://jamieduerden.me/post/monitoring-nginx-nagios/
* http://www.bogotobogo.com/DevOps/DevOps_Nginx_Nagios-Remote-Plugin-Executor-NRPE.php.NOT-Working
