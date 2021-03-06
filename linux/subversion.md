### Move existing repository to a new server
On the old server. Backup old repository
```shell
su svn
svnadmin dump /path/to/repository > repo_name.svn_dump
```
On the new server. Create new repository, import old repository data into the new one.
```shell
su svn
svnadmin create /path/to/repository
svnadmin load /path/to/repository < repo_name.svn_dump --force-uuid
```
**Note:** Dump and load do not copy conf subdirectory contents. Check contents of /conf/svnserve.conf and conf/passwd files after restore.

### Subversion over HTTPS with Apache
Install subversion, apache and create a directory to hold the repositories
```shell
apt install subversion apache2 libapache2-svn apache2-utils
mkdir /svn/repos/ -p
chown :www-data /svn/repos
# Make sure that UMASK 002 is set in /etc/login.defs for this to work
chmod g+rws /svn/repos
```

Add the following to `/etc/apache2/mods-enabled/dav_svn.conf`:
```
<Location /svn>
  DAV svn
  SVNParentPath /svn/repos
  AuthType Basic
  AuthName "Your repository name"
  AuthUserFile /svn/http-passwd
  Require valid-user
</Location>
```

Remove default site (2check):
```
a2dissite default
a2dissite default-ssl
???
apachectl graceful
```

Add users and passwords
```shell
# -c creates a new file and is needed for the first user only
htpasswd -c /svn/http-passwd user1
```

Create a repo and try to access it over HTTP on `http://serveraddress/svn/test/`
```
svnadmin create /svn/repos/test
service apache2 restart
```

Setup HTTPS
```
mkdir -p /etc/apache2/ssl
cp /path/to/cert/server.crt /etc/apache2/ssl
cp /path/to/cert/server.key /etc/apache2/ssl
chown :www-data /etc/apache2/ssl -R
chmod 640 /etc/apache2/ssl/*.*
a2enmod ssl
```
**Update** (not add) lines in `/etc/apache2/sites-available/default-ssl.conf`
```
SSLCertificateFile /etc/apache2/ssl/server.crt
SSLCertificateKeyFile /etc/apache2/ssl/server.key
```

Restart apache service
```
a2ensite default-ssl.conf
a2dissite 000-default.conf
# Comment out in /etc/apache2/ports.conf
# NameVirtualHost *:80  
# Listen 80
service apache2 restart
```
