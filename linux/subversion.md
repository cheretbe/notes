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

Setting up HTTPS
```
mkdir -p /etc/apache2/ssl
cp /path/to/cert/server.crt
cp /path/to/cert/server.key
chown :www-data /etc/apache2/ssl -R
chmod 640 /etc/apache2/ssl/*.*
a2enmod ssl
```
