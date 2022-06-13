* https://forums.raspberrypi.com/viewtopic.php?t=224493

View undervoltage log messages
```
journalctl -b 0 _KERNEL_SUBSYSTEM=hwmon
journalctl -f _KERNEL_SUBSYSTEM=hwmon
```

On `Raspberry Pi OS Lite (Debian 11)` network is managed by `ifupdown` and `dhcpcd`.
* https://github.com/cheretbe/notes/blob/master/linux/networking.md#dhcpcd
```shell
# Restart networking
# [?] Order of commands will be different depending on configuration change 
service networking restart
service dhcpcd restart
# After editing /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
```
* https://github.com/cheretbe/notes/blob/master/linux/networking.md#wlan

`/etc/wpa_supplicant/wpa_supplicant.conf` example:
```
country=RU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
	scan_ssid=1
	ssid="ssid"
	# password
	# https://github.com/cheretbe/notes/blob/master/linux/networking.md#wpa-psk
	psk=44116ea881531996d8a23af58b376d70f196057429c258f529577a26e727ec1b
}
```


* https://www.jeffgeerling.com/blog/2020/raspberry-pi-400-can-be-overclocked-22-ghz
* Flirc case
    * https://flirc.tv/collections/case/products/flirc-raspberrypi4-silver?variant=43085036454120
    * https://onpad.ru/catalog/cubie/raspberrypi/cases/3008.html?_openstat=bWFya2V0LnlhbmRleC5ydTvQkNC70Y7QvNC40L3QuNC10LLRi9C5INC60L7RgNC_0YPRgSBGbGlyYyDQtNC70Y8gUmFzcGJlcnJ5IFBpO1RsY1pJZklJQ0syelhUZVlHYjQxWmc7&ymclid=16068503486932583053300002
* https://github.com/TonyLHansen/raspberry-pi-safe-off-switch/
