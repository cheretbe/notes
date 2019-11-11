* http://attic.owncloud.org/download/repositories/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-owncloud-on-ubuntu-18-04

Use `https://download.owncloud.org/download/repositories/production/`

```shell
sudo su - www-data -s /bin/bash
/var/www/owncloud/occ app:disable files_videoplayer
```

* https://doc.owncloud.com/server/admin_manual/configuration/server/reverse_proxy_configuration.html
* https://doc.owncloud.com/server/admin_manual/configuration/server/harden_server.html

#### Client
* https://software.opensuse.org/download/package?project=isv:ownCloud:desktop&package=owncloud-client
```shell
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/Ubuntu_18.10/ /' > /etc/apt/sources.list.d/isv:ownCloud:desktop.list"
wget -nv https://download.opensuse.org/repositories/isv:ownCloud:desktop/Ubuntu_18.10/Release.key -O Release.key
sudo apt-key add - < Release.key
sudo apt-get update
sudo apt-get install owncloud-client
```


#### Headless linux client
* https://blog.caroga.net/how-to-synchronize-your-files-with-transips-stack-using-the-commandline/
  * Uses webdav, is any good for large files (??)
