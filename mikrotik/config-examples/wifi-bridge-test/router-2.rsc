# jul/06/2018 07:33:01 by RouterOS 6.41.4
# model = RouterBOARD mAP 2nD
/interface bridge
add fast-forward=no name=bridge1
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
add authentication-types=wpa-psk,wpa2-psk eap-methods="" \
    management-protection=allowed mode=dynamic-keys name=profile1 \
    supplicant-identity="" wpa-pre-shared-key=1234567890 wpa2-pre-shared-key=\
    1234567890
/interface wireless
set [ find default-name=wlan1 ] band=2ghz-b/g/n channel-width=20/40mhz-Ce \
    disabled=no distance=indoors frequency=2442 mode=station-wds \
    security-profile=profile1 ssid=bridge-test wds-default-bridge=bridge1 \
    wds-mode=dynamic wireless-protocol=nv2-nstreme-802.11
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
/ip dhcp-client
add dhcp-options=hostname,clientid disabled=no interface=bridge1
/system clock
set time-zone-name=Europe/Kaliningrad
/system identity
set name=map2nd
