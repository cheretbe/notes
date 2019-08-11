 * http://www.easy2boot.com/download/
 * http://www.easy2boot.com/make-an-easy2boot-usb-drive/make-using-linux/
 * [Custom background](../images/MyBackground.jpg) (save as `_ISO\MyBackground.jpg`)
 
 ### .imgPTN Files
 * Download MPI Tool Kit: http://www.easy2boot.com/add-payload-files/makepartimage
 * Install ImDisk from `\ImDisk\imdiskinst.exe` (**reinstall** on upgrade)
 * Run `MakePartImage.cmd` as Administrator
 
 Suggested temporary ImDisk drive size is in MB (10^6 bytes), not MiB<br>
 To calculate size adjustment (assuming that util directory size is 28 **MiB**
 ```Powershell
(28Mb - (get-WmiObject win32_logicaldisk -Filter "DeviceID='U:'").FreeSpace) / 1000 / 1000
 ```
 
 Switch partitions when booting or using `_ISO\SWITCH_E2B.exe` (or `e2b\SWITCH_E2B.exe`) on Windows (works with NTFS USB drives only)
 
 ### ISO files
 
 * Antivirus
     * DrWeb: https://free.drweb.com/aid_admin/?lng=en
     * Kaspersky Rescue Disk: https://support.kaspersky.com/us/viruses/rescuedisk
 * Utilities
     * Clonezilla: http://clonezilla.org/downloads.php
     * GParted: https://gparted.org/download.php
     * TeraByte Image for Linux: https://www.terabyteunlimited.com/image-for-linux.htm
 * Linux
     * List of releases: https://wiki.ubuntu.com/Releases
     * Ubuntu release cycle: https://ubuntu.com/about/release-cycle
     * Ubuntu Releases: http://releases.ubuntu.com/
     * Ubuntu 19.04 Desktop x64: http://releases.ubuntu.com/19.04/ubuntu-19.04-desktop-amd64.iso
     * ~~Ubuntu 17.10.1 Desktop x64: http://releases.ubuntu.com/17.10.1/ubuntu-17.10.1-desktop-amd64.iso~~
     * Ubuntu 18.04.3 Desktop x64: http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-desktop-amd64.iso
     * Ubuntu 16.04.6 Desktop x64: http://releases.ubuntu.com/16.04.6/ubuntu-16.04.6-desktop-amd64.iso
     * Ubuntu 18.04.3 Server x64 (live CD): http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-live-server-amd64.iso
     * Ubuntu 18.04.3 Server x64: http://cdimage.ubuntu.com/releases/18.04.3/release/ubuntu-18.04.3-server-amd64.iso
     * Ubuntu 16.04.6 Server x64: http://releases.ubuntu.com/16.04.6/ubuntu-16.04.6-server-amd64.iso
     * ~~Ubuntu 14.04.5 Server x64: http://releases.ubuntu.com/14.04.5/ubuntu-14.04.5-server-amd64.iso~~
     * Xubuntu 18.04.3 x64: https://mirror.yandex.ru/ubuntu-cdimage/xubuntu/releases/18.04/release/xubuntu-18.04.3-desktop-amd64.iso
     * Xubuntu 16.04.3 x86: https://mirror.yandex.ru/ubuntu-cdimage/xubuntu/releases/18.04/release/xubuntu-18.04.3-desktop-i386.iso
     * Xubuntu 16.04.6 x64: https://mirror.yandex.ru/ubuntu-cdimage/xubuntu/releases/16.04/release/xubuntu-16.04.6-desktop-amd64.iso
     * Xubuntu 16.04.6 x86: https://mirror.yandex.ru/ubuntu-cdimage/xubuntu/releases/16.04/release/xubuntu-16.04.6-desktop-i386.iso
     * Kubuntu 18.04.3 x64: https://mirror.yandex.ru/ubuntu-cdimage/kubuntu/releases/18.04.3/release/kubuntu-18.04.3-desktop-amd64.iso
     * ~~Kubuntu 17.10.1 x64: http://cdimage.ubuntu.com/kubuntu/releases/17.10.1/release/kubuntu-17.10.1-desktop-amd64.iso~~
     * CentOS release "end of life": https://wiki.centos.org/FAQ/General#head-fe8a0be91ee3e7dea812e8694491e1dde5b75e6d
     * CentOS-7 (1810) Release Notes: https://wiki.centos.org/Manuals/ReleaseNotes/CentOS7.1810?action=show&redirect=Manuals%2FReleaseNotes%2FCentOS7
     * CentOS 7.6 x64 Gnome: https://mirror.yandex.ru/centos/7/isos/x86_64/CentOS-7-x86_64-LiveGNOME-1810.iso
     * CentOS 7.6 x64 KDE: https://mirror.yandex.ru/centos/7/isos/x86_64/CentOS-7-x86_64-LiveKDE-1810.iso
     * CentOS 6.9 i386: https://mirror.yandex.ru/centos/6.9/isos/i386/CentOS-6.9-i386-LiveDVD.iso
