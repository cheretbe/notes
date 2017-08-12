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
transmission-cli --download-dir ~/Downloads http://releases.ubuntu.com/16.04/ubuntu-16.04.3-server-amd64.iso.torrent
# or (package aria2 or https://aria2.github.io/)
aria2c --seed-time 0 --dir=~/Downloads http://releases.ubuntu.com/16.04/ubuntu-16.04.3-server-amd64.iso.torrent

mkdir -p ~/temp/ubuntu-iso
# requires root privileges
# mount -o loop ~/Downloads/ubuntu-16.04.2-server-amd64.iso ~/temp/ubuntu-iso
fuseiso ~/Downloads/ubuntu-16.04.2-server-amd64.iso ~/temp/ubuntu-iso
mkdir -p ~/temp/ubuntu-temp-iso
# -R, -r, --recursive          copy directories recursively
# -T, --no-target-directory    treat DEST as a normal file
cp -rT ~/temp/ubuntu-iso ~/temp/ubuntu-temp-iso
# Fix readonly CD-ROM attributes
find ~/temp/ubuntu-temp-iso/ -type d -exec chmod 755 {} \;
find ~/temp/ubuntu-temp-iso/ -type f -exec chmod 644 {} \;
# requires root privileges
# umount ~/temp/ubuntu-iso
fusermount -u ~/temp/ubuntu-iso
rmdir ~/temp/ubuntu-iso

cp ~/temp/ubuntu-temp-iso/isolinux/txt.cfg{,.bak}
cp ~/temp/unattend_ubuntu_isolinux.cfg ~/temp/ubuntu-temp-iso/isolinux/txt.cfg
cp ~/temp/unattend_ubuntu_srv.preseed ~/temp/ubuntu-temp-iso/npa.preseed

#   -D, -disable-deep-relocation (??????)
#                                  Disable deep directory relocation (violates ISO9660)
# -r, -rational-rock               Generate rationalized Rock Ridge directory information
# -V ID, -volid ID                 Set Volume ID
# -cache-inodes                    Cache inodes (needed to detect hard links)
# -J, -joliet                      Generate Joliet directory information
# -l, -full-iso9660-filenames      Allow full 31 character filenames for ISO9660 names
# -b FILE, -eltorito-boot FILE     Set El Torito boot image name
# -c FILE, -eltorito-catalog FILE  Set El Torito boot catalog name
# -no-emul-boot                    Boot image is 'no emulation' image
# -boot-load-size #                Set numbers of load sectors
# -boot-info-table                 Patch boot image with info table
# -o FILE, -output FILE            Set output file name

mkisofs -D -r -V "UNATTENDED_UBUNTU" -cache-inodes -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ~/temp/unattended-ubuntu-16.04.2-server-amd64.iso ~/temp/ubuntu-temp-iso

```

http://searchitchannel.techtarget.com/feature/Performing-an-automated-Ubuntu-install-using-preseeding


* http://askubuntu.com/questions/806820/how-do-i-create-a-completely-unattended-install-of-ubuntu-desktop-16-04-1-lts
* http://askubuntu.com/questions/595826/how-to-create-ubuntu-installation-preseed-file
* http://unix.stackexchange.com/questions/139814/what-values-from-debconf-get-selections-should-not-be-preseeded
* https://help.ubuntu.com/lts/installation-guide/example-preseed.txt
