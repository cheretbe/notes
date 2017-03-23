### Ubuntu Server
The Ubuntu Installer supports automating installs via preconfiguration files (preseeding). Official [guide](https://help.ubuntu.com/16.04/installation-guide/amd64/apb.html).


Although most questions used by debian-installer can be preseeded using this method, there are some notable exceptions.
You must (re)partition an entire disk or use available free space on a disk; it is not possible to use existing partitions.

* http://askubuntu.com/questions/806820/how-do-i-create-a-completely-unattended-install-of-ubuntu-desktop-16-04-1-lts
* http://askubuntu.com/questions/595826/how-to-create-ubuntu-installation-preseed-file
* http://unix.stackexchange.com/questions/139814/what-values-from-debconf-get-selections-should-not-be-preseeded
* https://help.ubuntu.com/lts/installation-guide/example-preseed.txt
