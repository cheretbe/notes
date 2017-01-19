Install subversion, apache and create a directory to hold repositories
```shell
apt install subversion apache2 libapache2-svn apache2-utils
mkdir /svn/repos/ -p
chown :www-data /svn/repos
# Make sure that UMASK 002 is set in /etc/login.defs for this to work
chmod g+rws /svn/repos
```
