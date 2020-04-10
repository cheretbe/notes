TAP adapter to try on Windows 7 with driver signature problems: https://build.openvpn.net/downloads/releases/tap-windows-9.21.2.exe

```bat
:: List TAP adapters
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" hwids tap*

:: Remove adapter
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" remove tap0901

:: Create adapter
"C:\Program Files\TAP-Windows\bin\tapinstall.exe" install "C:\Program Files\TAP-Windows\driver\OemVista.inf" tap0901


"C:\Program Files\OpenVPN\bin\openvpn.exe" --show-adapters
"C:\Program Files\OpenVPN\bin\openvpn.exe" --show-net
```
