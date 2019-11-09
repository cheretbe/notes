* http://attic.owncloud.org/download/repositories/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-owncloud-on-ubuntu-18-04

Use `https://download.owncloud.org/download/repositories/production/`

```shell
sudo su - www-data -s /bin/bash
/var/www/owncloud/occ app:disable files_videoplayer
```

* https://doc.owncloud.com/server/admin_manual/configuration/server/reverse_proxy_configuration.html
* https://doc.owncloud.com/server/admin_manual/configuration/server/harden_server.html

Headless linux client
* https://blog.caroga.net/how-to-synchronize-your-files-with-transips-stack-using-the-commandline/
  * Uses webdav, is any good for large files (??)
