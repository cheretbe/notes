* https://www.zabbix.com/life_cycle_and_release_policy
* https://www.zabbix.com/documentation/4.0/manual/installation/install_from_packages/debian_ubuntu

```shell
# Ubuntu 18.04
apt install apache2 libapache2-mod-php \
            php php-pear php-cgi php-common libapache2-mod-php php-mbstring php-net-socket php-gd \
            php-mysql php-gettext php-bcmath \
            mariadb-server
            
mysql_secure_installation

wget https://repo.zabbix.com/zabbix/4.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_4.0-2+bionic_all.deb
dpkg -i zabbix-release_4.0-2+bionic_all.deb
apt update

apt install zabbix-server-mysql zabbix-frontend-php zabbix-agent zabbix-get
```
