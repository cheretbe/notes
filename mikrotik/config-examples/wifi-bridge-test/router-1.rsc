# jul/06/2018 07:41:24 by RouterOS 6.42
# model = RouterBOARD D52G-5HacD2HnD-TC
/interface bridge
add fast-forward=no name=bridge1
/interface wireless
set [ find default-name=wlan1 ] band=2ghz-b/g/n channel-width=20/40mhz-Ce \
    disabled=no frequency=2442 mode=bridge radio-name=br-test ssid=\
    bridge-test wds-default-bridge=bridge1 wds-mode=dynamic \
    wireless-protocol=nv2
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
add authentication-types=wpa-psk,wpa2-psk eap-methods="" \
    management-protection=allowed mode=dynamic-keys name=profile1 \
    supplicant-identity="" wpa-pre-shared-key=1234567890 wpa2-pre-shared-key=\
    1234567890
/interface wireless
set [ find default-name=wlan2 ] band=5ghz-a/n mode=bridge security-profile=\
    profile1 ssid=mt-bridge wds-default-bridge=bridge1 wds-mode=dynamic
/ip hotspot profile
set [ find default=yes ] html-directory=flash/hotspot
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether3
add bridge=bridge1 interface=ether4
add bridge=bridge1 interface=ether5
/ip dhcp-client
add dhcp-options=hostname,clientid disabled=no interface=bridge1
/system clock
set time-zone-name=Europe/Kaliningrad
/system identity
set name=ac2
/system routerboard settings
set silent-boot=no
