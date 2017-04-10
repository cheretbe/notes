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

cd nagios-4.3.1/
# [!] Change nagios-4.3.1 to current version
./configure --prefix=/usr/local/nagios-4.3.1 --sysconfdir=/etc/nagios --with-nagios-group=nagios --with-command-group=nagcmd

make all
make install
make install-init
make install-config
make install-commandmode
make install-webconf
```

* https://assets.nagios.com/downloads/nagioscore/docs/Installing_Nagios_Core_From_Source.pdf
* https://assets.nagios.com/downloads/nagioscore/docs/Nagios-Core-Installing-On-Centos7.pdf
* http://idroot.net/linux/install-nagios-ubuntu-16-04/
* http://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/install-nagios-4-1-1-ubuntu-16-04.html
* ~~https://jamieduerden.me/post/monitoring-nginx-nagios/~~
* ~~http://www.bogotobogo.com/DevOps/DevOps_Nginx_Nagios-Remote-Plugin-Executor-NRPE.php.NOT-Working~~
