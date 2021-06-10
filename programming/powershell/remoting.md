## Powershell Remoting

* References
    * https://adamtheautomator.com/psremoting/
    * **https://github.com/PowerShell/PowerShell/issues/3708**
    * https://stackoverflow.com/questions/2985032/powershell-remoting-profiles
    * https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#host-requirements
    * https://blog.ipswitch.com/the-infamous-double-hop-problem-in-powershell
* [HTTPS with a self-signed SSL certificate](#https-with-a-self-signed-ssl-certificate)

```powershell
$credential = Get-Credential
Enter-PSSession -ComputerName "host.domain.tld" -Credential $credential
Enter-PSSession -UseSSL -ComputerName "host.domain.tld" -Credential "user" 2>&1
Invoke-Command -UseSSL -SessionOption (New-PSSessionOption -SkipCACheck -SkipCNCheck -SkipRevocationCheck) `
  -ComputerName "localhost" -Credential $credential -ScriptBlock { & cmd /c set }
  
# View current authentication type (on remote host)
$PSSenderInfo.UserInfo.Identity.AuthenticationType
  
Invoke-Command -ComputerName "host.domain.tld" -ScriptBlock { Register-PSSessionConfiguration -Name "domain_user" -RunAsCredential "domain\user" -Force }
Enter-PSSession -ComputerName "host.domain.tld" -ConfigurationName "domain_user"

# On a remote host
Get-PSSessionConfiguration
Unregister-PSSessionConfiguration "domain_user"
```

### HTTPS with a self-signed SSL certificate
* https://4sysops.com/archives/powershell-remoting-over-https-with-a-self-signed-ssl-certificate/
* http://www.hurryupandwait.io/blog/understanding-and-troubleshooting-winrm-connection-and-authentication-a-thrill-seekers-guide-to-adventure

```powershell
$Cert = New-SelfSignedCertificate -CertstoreLocation Cert:\LocalMachine\My -DnsName "myhost"
# or
$Cert = New-SelfSignedCertificate -CertstoreLocation Cert:\LocalMachine\My -DnsName "myhost" -NotAfter (Get-Date).AddYears(10)

Export-Certificate -Cert $Cert -FilePath C:\temp\myhost.cer
```
By default `New-SelfSignedCertificate` creates a certificate that is valid for one year. To create a certificate that lasts longer use `-NotAfter (Get-Date).AddYears(5)` parameter. The problem is that this parameter doesn't work on Win8.1/Win2012R2 (even with PS 5.1 installed):  https://social.technet.microsoft.com/Forums/windowsserver/en-US/cd5bba06-5931-42ee-afad-1e438b3df759/problem-generating-a-certificate-for-ldaps-using-newselfsignedcertificate-quota-parameter?forum=winserver8gen

The solution is to use openssl:

```shell
# EKU should contain serverAuth and this parameter can't be passed as a command-line option
# We create a temporary config file to add it
cp /usr/lib/ssl/openssl.cnf ./ext_config.cnf

# Windows version
copy "C:\Program Files\Common Files\SSL\openssl.cnf" ext_config.cnf
```
Add the following to `ext_config.cnf`:
```
[myextensions]
extendedKeyUsage = serverAuth,clientAuth
```
```shell
# Create a self-signed certificate
openssl req \
       -newkey rsa:2048 -nodes -keyout myhost.key \
       -x509 -days 3650 -out myhost.crt \
       -extensions myextensions -config ext_config.cnf
```
When using own SSL CA create CSR as described [here](https://github.com/cheretbe/notes/blob/master/ssl.md#own-ssl-certificate-authority), then create `winrm_server_ext.cnf` file with the following content
```
[winrm_server_ext]
extendedKeyUsage = serverAuth,clientAuth
```
and use `-extensions` and `-extfile` options on signing 
```shell
openssl x509 -req -extensions winrm_server_ext -extfile winrm_server_ext.cnf -in myhost.csr -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -out myhost.crt -days 3650
```

```shell
# Take a private key (myhost.key) and a certificate (myhost.crt), and combine them into a PKCS12 file (myhost.pfx):
openssl pkcs12 \
       -inkey myhost.key \
       -in myhost.crt \
       -export -out myhost.p12
```

Copy `myhost.p12` to a Windows machine
```batch
:: Non-Interactive commands (Useful when using PSExec)
:: Check if root CA certificate is installed
powershell -NonInteractive "Get-ChildItem 'Cert:\LocalMachine\Root' | Where-Object {$_.Thumbprint -eq (New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 ".\root_ca.crt").Thumbprint}"
```
```powershell
# When using own SSL CA import it's root certificate
# It's not strictly necessary for WinRM to work, but will help when checking server certificate properties
Import-Certificate -FilePath "root_ca.crt" -CertStoreLocation "Cert:\LocalMachine\Root"

# View certificate list
Get-ChildItem "Cert:\LocalMachine\My" | Format-List

# Import the certificate to "Certificates (Local Computer)" > "Personal"
$Cert = Import-PfxCertificate -FilePath "c:\temp\myhost.p12" -CertStoreLocation "Cert:\LocalMachine\My" -Exportable
# Delete a certificate (in case something went wrong)
Get-ChildItem "Cert:\LocalMachine\My" | Where-Object { $_.Thumbprint -eq $Cert.Thumbprint } | Remove-Item
```
Windows 7 doesn't have `Import-PfxCertificate`, use `certutil -importpfx c:\temp\myhost.12`

```powershell
#  -SkipNetworkProfileCheck -Force
Enable-PSRemoting

# Delete HTTP listener (optional)
Get-ChildItem WSMan:\Localhost\listener | Where -Property Keys -eq "Transport=HTTP" | Remove-Item -Recurse
# Delete all listeners
Remove-Item -Path WSMan:\Localhost\listener\listener* -Recurse

New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint $Cert.Thumbprint –Force
# or
New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint "0000000000000000000000000000000000000000" –Force
# View listeners
dir wsman:\localhost\listener

# Enable HTTPS port in the firewall
New-NetFirewallRule -DisplayName "Windows Remote Management (HTTPS-In)" -Name "WINRM-HTTPS-In-TCP-NoScope" -Profile Any -LocalPort 5986 -Protocol TCP
New-NetFirewallRule -DisplayName "Удаленное управление Windows (HTTPS - входящий трафик)" -Name "WINRM-HTTPS-In-TCP-NoScope" -Profile Any -LocalPort 5986 -Protocol TCP
# Disable HTTP port (optional)
Disable-NetFirewallRule -DisplayName "Windows Remote Management (HTTP-In)"
Disable-NetFirewallRule -DisplayName "Удаленное управление Windows (HTTP - входящий трафик)"

# Windows 7 doesn't have New-NetFirewallRule, use netsh instead
netsh advfirewall firewall add rule name="Windows Remote Management (HTTPS-In)" dir=in action=allow protocol=TCP localport=5986

Test-WSMan -useSSL myhost
winrs -r:https://myhost:5986/wsman -u:vagrant -p:vagrant ipconfig
```

On a client computer
```powershell
Import-Certificate -Filepath "C:\temp\myhost.cer" -CertStoreLocation "Cert:\LocalMachine\Root"
# When using own CA import CA certificate instead
Import-Certificate -Filepath "C:\temp\ca.cert.crt" -CertStoreLocation "Cert:\LocalMachine\Root"
Enter-PSSession -ComputerName myHost -UseSSL -Credential (Get-Credential)
# Windows 7
certutil -addstore "Root" "C:\temp\ca.cert.crt"
```



pywinrm (https://github.com/diyan/pywinrm)
```shell
pip install pywinrm
# For Kerberos auth
pip install pywinrm requests_kerberos
```
```python
import winrm
s = winrm.Session('https://host.domain.tld:5986', auth=('user', 'password'), ca_trust_path='/etc/ssl/certs', transport='ntlm')
r = s.run_cmd('ipconfig', ['/all'])
r = s.run_ps("""
  & cmd /c ver
""")
# print(r.std_out.decode("windows-1251"))
print(r.std_out.decode("cp866"))

# Domain member
s = winrm.Session('host.domain.tld', auth=('', ''), transport='kerberos')
```
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#[System.Text.Encoding]::Default
```

```shell
pip install pypsrp
# For Kerberos auth
pip install pypsrp[kerberos]
```

```python
from pypsrp.client import Client
# Domain member
client = Client("host.domain.tld", ssl=False, auth='kerberos')
# Self-signed SSL
os.environ['REQUESTS_CA_BUNDLE']="/etc/ssl/certs"
client = Client("host.domain.tld", username="user", password="pwd")

stdout, stderr, rc = client.execute_cmd("cmd /c ver", encoding="1251")
client.copy("/path/to/script.ps1", 'c:\\temp\\script.ps1')
```

#### Linux
* https://gbe0.com/posts/linux/desktop/linux-powershell-remote-to-windows-with-docker/

```powershell
Install-Module -Name PSWSMan -Force
Install-WSMan

$cred = Get-Credential
Enter-PSSession -ComputerName my-computer -Credential $cred
```

#### Unencrypted

:bangbang: For testing environments only, don't use these settings in production

On server
```powershell
# Windows 7 doesn't have Get-NetConnectionProfile and Set-NetConnectionProfile
# Need to download custom script first
# https://www.peppercrew.nl/index.php/2016/02/change-network-connection-category-using-powershell/
(New-Object -TypeName System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/ITMicaH/Powershell-functions/master/Windows/Network/NetConnectionProfiles.ps1", "$env:temp\NetConnectionProfiles.ps1")
Set-ExecutionPolicy Bypass -Scope Process -Force
. "$env:temp\NetConnectionProfiles.ps1"

# Set all network connections to private
Get-NetConnectionProfile -NetworkCategory Public | Set-NetConnectionProfile -NetworkCategory Private

# -quiet: no prompts
# -force: enable even if public network is present
# winrm quickconfig [-quiet] [-force]
Enable-PSRemoting
# No prompts
Enable-PSRemoting -Force
# Enable even if public network is present
Enable-PSRemoting -SkipNetworkProfileCheck -Force
# Test if a computer can run remote commands
Test-WSMan [-ComputerName SRV1]

# Test connection on localhost
# winrs seems to work without setting winrm/config/client
winrs -r:http://localhost:5985/wsman -u:vagrant -p:vagrant ipconfig

winrm set winrm/config/client @{AllowUnencrypted="true"}
Enter-PSSession -ComputerName "localhost" -Credential vagrant -Authentication basic 2>&1
```

On client
```powershell
Set-Item "wsman:\localhost\Client\TrustedHosts" -Value "*" -Force
# Default WinRM port: 5985
# Enter-PSSession -ComputerName localhost -port 1111 -Credential vagrant
# This will prompt for a password
Enter-PSSession -ComputerName "hostname" -Credential "vagrant" 2>&1
# This will not
$pwd = ConvertTo-SecureString "vagrant" -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential @("vagrant", $pwd)
Enter-PSSession -ComputerName "hostname" -Credential $credential 2>&1
# Prompt for credential and save it for later use
$credential = Get-Credential
# Run scriptblock
Invoke-Command -ComputerName "hostname" -Credential $credential -ScriptBlock { & cmd /c set }
# Save/load credentials
$credential | Export-CliXml -Path "C:\My\Path\cred.xml"
$credential = Import-CliXml -Path "C:\My\Path\cred.xml"
# or
$credential.Password | ConvertFrom-SecureString | Out-File "C:\My\Path\pwd.txt"
$pwd = (Get-Content "C:\My\Path\pwd.txt" | ConvertTo-SecureString)
```
