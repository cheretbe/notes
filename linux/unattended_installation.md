### Ubuntu Server
The Ubuntu Installer supports automating installs via preconfiguration files (preseeding). Official [guide](https://help.ubuntu.com/16.04/installation-guide/amd64/apb.html).


Although most questions used by debian-installer can be preseeded using this method, there are some notable exceptions.
You must (re)partition an entire disk or use available free space on a disk; it is not possible to use existing partitions.


View current installation settings (contain extra stuff, should be used for reference only)
```bash
sudo apt-get install debconf-utils
sudo debconf-get-selections --installer
# Packages config
sudo debconf-get-selections
```
ISO creation
```bash
mkdir -p ~/temp/ubuntu-iso
mount -o loop ~/Downloads/ubuntu-16.04.2-server-amd64.iso ~/temp/ubuntu-iso
mkdir -p ~/temp/ubuntu-temp-iso
# -R, -r, --recursive          copy directories recursively
# -T, --no-target-directory    treat DEST as a normal file
cp -rT ~/temp/ubuntu-iso ~/temp/ubuntu-temp-iso
```

http://searchitchannel.techtarget.com/feature/Performing-an-automated-Ubuntu-install-using-preseeding


* http://askubuntu.com/questions/806820/how-do-i-create-a-completely-unattended-install-of-ubuntu-desktop-16-04-1-lts
* http://askubuntu.com/questions/595826/how-to-create-ubuntu-installation-preseed-file
* http://unix.stackexchange.com/questions/139814/what-values-from-debconf-get-selections-should-not-be-preseeded
* https://help.ubuntu.com/lts/installation-guide/example-preseed.txt
