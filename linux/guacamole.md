* https://guacamole.incubator.apache.org/doc/gug/installing-guacamole.html
* https://guacamole.incubator.apache.org/doc/gug/users-guide.html
* https://www.chasewright.com/guacamole-with-mysql-on-ubuntu/
* https://www.chasewright.com/guacamole-upgrade/#comment-595 (wait for a reply)

ln -s /etc/guacamole /usr/share/tomcat8/.guacamole
 
echo "mysql-hostname: localhost" >> /etc/guacamole/guacamole.properties
echo "mysql-port: 3306" >> /etc/guacamole/guacamole.properties
echo "mysql-database: guacamole_db" >> /etc/guacamole/guacamole.properties
echo "mysql-username: guacamole_user" >> /etc/guacamole/guacamole.properties
echo "mysql-password: <password>" >> /etc/guacamole/guacamole.properties
```
mysql-hostname: localhost
mysql-port: 3306
mysql-database: guacamole_db
mysql-username: guacamole_user
mysql-password: <password>
```
 
cat guacamole-auth-jdbc-0.9.11-incubating/mysql/schema/*.sql | mysql -u root -p<password> guacamole_db
