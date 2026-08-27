# Powershell Remoting

* References
    * https://adamtheautomator.com/psremoting/
    * **https://github.com/PowerShell/PowerShell/issues/3708**
    * https://stackoverflow.com/questions/2985032/powershell-remoting-profiles
    * https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#host-requirements
    * **https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html**
    * https://blog.ipswitch.com/the-infamous-double-hop-problem-in-powershell
* [HTTPS with a self-signed SSL certificate](#https-with-a-self-signed-ssl-certificate)
* [Linux](#linux)
* [Unencrypted](#unencrypted)

## Linux client

### Native

* :bulb: See docker version below

```shell
# Tested on Ubuntu 24.04 (noble)
# 1. Microsoft package repo
sudo apt update && sudo apt install -y wget apt-transport-https
wget -q https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb
sudo apt update

# 2. PowerShell (currently 7.6.5)
sudo apt install -y powershell

# 3. GSSAPI NTLM mechanism — required for Negotiate against local Windows accounts
sudo apt install -y gss-ntlmssp
  
# 4. WSMan client libraries — not shipped in PowerShell's Linux builds
sudo pwsh -NoProfile -c "Install-Module PSWSMan -Scope AllUsers -Force -AcceptLicense; Import-Module PSWSMan; Install-WSMan"
# Verify:
pwsh -NoProfile -c 'Import-Module PSWSMan; Get-WSManVersion'
ls /etc/gss/mech.d/mech.ntlmssp.conf
```
```powershell
pwsh
$cred = Get-Credential
# Non-HTTPS port 5985
Enter-PSSession -ComputerName host.domain.tld -Port 5985 -Authentication Negotiate -Credential $cred
# HTTPS port 5986
# [!] See the fix for "SPNEGO cannot find mechanisms to negotiate" below
Enter-PSSession -UseSSL -ComputerName host.domain.tld -Credential $cred
```
-UseSSL failure fix
```shell
# Enter-PSSession: Connecting to remote server host.domain.tld failed with the following error
# message : acquiring creds with username only failed An invalid name was supplied SPNEGO cannot
# find mechanisms to negotiate For more information, see the about_Remote_Troubleshooting Help topic.
# 
# Root Cause: Ubuntu 22.04 ships ancient gss-ntlmssp v0.7.0 (2021) with credential-passing bug
# Solution: Upgrade to gss-ntlmssp v1.3.1 (2024)

# Install build dependencies
sudo apt-get update
sudo apt-get install -y autoconf automake libtool libkrb5-dev doxygen \
    libwbclient-dev libssl-dev libunistring-dev docbook-xsl xsltproc \
    git build-essential

# Clone and build gss-ntlmssp v1.3.1
cd /tmp
git clone --depth 1 --branch v1.3.1 https://github.com/gssapi/gss-ntlmssp.git
cd gss-ntlmssp
autoreconf -f -i
./configure --prefix=/usr
make
sudo make install

# Update GSSAPI to use new library (backup the original config)
sudo cp /etc/gss/mech.d/mech.ntlmssp.conf{,.bak}
sudo tee /etc/gss/mech.d/mech.ntlmssp.conf > /dev/null << 'EOF'
# NTLMSSP mechanism plugin v1.3.1
gssntlmssp_v1		1.3.6.1.4.1.311.2.2.10	        /usr/lib/gssntlmssp/gssntlmssp.so
EOF
```

### Docker

Dockerfile
```
# PowerShell with working WinRM/PSRemoting against Windows hosts.
#
# Three things are needed beyond a stock PowerShell install, none of which the
# powershell package pulls in:
#   1. PowerShell itself from packages.microsoft.com. The MCR powershell images
#      are deprecated and frozen at 7.6.0-preview.3 (Feb 2025); the apt repo is
#      current.
#   2. gss-ntlmssp, so SPNEGO has an NTLM mechanism to offer. Without it,
#      Negotiate against a local Windows account fails with
#      "SPNEGO cannot find mechanisms to negotiate".
#   3. PSWSMan, which supplies libmi.so/libpsrpclient.so. Without them,
#      New-PSSession fails with "no supported WSMan client library was found".
#
# gss-ntlmssp is built from source rather than installed from apt: the version
# in Ubuntu 22.04 (0.7.x, 2021) does not work with libmi.

########################  stage 1 — build gss-ntlmssp  ########################
FROM ubuntu:24.04 AS ntlm-builder

ARG GSS_NTLMSSP_VERSION=v1.3.1

RUN apt-get update && apt-get install -y --no-install-recommends \
        autoconf automake libtool build-essential git ca-certificates \
        pkg-config gettext \
        libkrb5-dev libwbclient-dev libssl-dev libunistring-dev zlib1g-dev \
        docbook-xml docbook-xsl xsltproc libxml2-utils doxygen \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch "${GSS_NTLMSSP_VERSION}" \
        https://github.com/gssapi/gss-ntlmssp.git /src

WORKDIR /src
RUN autoreconf -f -i \
    && ./configure --prefix=/usr \
    && make -j"$(nproc)" \
    && make install DESTDIR=/out

############################  stage 2 — runtime  ##############################
FROM ubuntu:24.04

# powershell | powershell-lts | powershell-preview
ARG PS_PACKAGE=powershell

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates wget apt-transport-https \
        libgssapi-krb5-2 libkrb5-3 libwbclient0 libunistring5 libssl3t64 \
    && wget -q https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends "${PS_PACKAGE}" \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ntlm-builder /out/ /

# --prefix=/usr puts the plugin outside the multiarch dir, so the mech config
# has to name that path explicitly.
RUN mkdir -p /etc/gss/mech.d \
    && printf '%s\n' \
        '# NTLMSSP mechanism plugin, built from source' \
        'gssntlmssp_v1  1.3.6.1.4.1.311.2.2.10  /usr/lib/gssntlmssp/gssntlmssp.so' \
        > /etc/gss/mech.d/mech.ntlmssp.conf \
    && ldconfig

RUN pwsh -NoProfile -Command "\
        \$ErrorActionPreference = 'Stop'; \
        Install-Module PSWSMan -Scope AllUsers -Force -AcceptLicense; \
        Import-Module PSWSMan; \
        Install-WSMan; \
        Get-WSManVersion"

# Run as a non-root user matching the host uid/gid, so files written to a
# bind-mounted home stay readable on the host. ubuntu:24.04 ships a default
# "ubuntu" user squatting on 1000:1000, so drop it first.
ARG USER_UID=1000
ARG USER_GID=1000

RUN userdel -r ubuntu 2>/dev/null || true \
    && groupdel ubuntu 2>/dev/null || true \
    && groupadd -g "${USER_GID}" pwsh \
    && useradd -m -u "${USER_UID}" -g "${USER_GID}" pwsh

USER pwsh
WORKDIR /home/pwsh

CMD ["pwsh"]
```

```shell
mkdir -p ~/temp/pwsh-docker-build
cd ~/temp/pwsh-docker-build
nano Dockerfile
docker build --network host --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t local/pwsh-winrm:latest .
# [!!] Important to create the dir before the first run (otherwise it will be owned by root)
mkdir -p ${HOME}/temp/powershell-home
docker run -dti --network host -v ${HOME}/temp/powershell-home:/home/pwsh --name powershell local/pwsh-winrm:latest bash
docker exec -it powershell pwsh
```



Attempts to find working replacement for linux screen
```powershell
# https://devops-collective-inc.gitbook.io/secrets-of-powershell-remoting/session-management

$job = Start-Job { write-output "1"; start-sleep 10; write-output "2"; start-sleep 10; write-output "3" }

$job.State

# -Keep parameter preserves the state of the aggregated streams of a job so
# that it can be viewed again. Without this parameter all aggregated stream
# data is erased when the job is received.
$job | Receive-Job -Keep

# -Wait instructs to wait until all job results are received. Erases stream data.
# -Wait and -Keep are mutually exclusive :(
$job | Receive-Job -Wait
```

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
:: If version 2.30+ fails to connect with the following error:
:: Logon failure: the user has not been granted the requested logon type at this computer.
:: The solution is to use -i option

:: Check if root CA certificate is installed
powershell -NonInteractive "Get-ChildItem 'Cert:\LocalMachine\Root' | Where-Object {$_.Thumbprint -eq (New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 ".\root_ca.crt").Thumbprint}"
:: List server certificates
powershell -NonInteractive "Get-ChildItem 'Cert:\LocalMachine\My' | Format-List"

# Import CA certificate
powershell -NonInteractive "Import-Certificate -FilePath '.\root_ca.crt' -CertStoreLocation 'Cert:\LocalMachine\Root'"
# Import host's certificate
powershell -NonInteractive "Import-PfxCertificate -FilePath '.\host.domain.tld.p12' -CertStoreLocation 'Cert:\LocalMachine\My' -Exportable"

:: Enable WinRM
winrm quickconfig -quiet

:: View listeners 
powershell -NonInteractive "Get-ChildItem WSMan:\Localhost\listener"

:: Delete HTTP listener
powershell -NonInteractive "Get-ChildItem WSMan:\Localhost\listener | Where -Property Keys -eq 'Transport=HTTP' | Remove-Item -Recurse"

:: Add HTTPS listener
powershell -NonInteractive "New-Item -Path WSMan:\LocalHost\Listener -Transport HTTPS -Address * -CertificateThumbPrint (New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 '.\host.domain.tld.p12').Thumbprint –Force"

:: Disable HTTP port
powershell -NonInteractive "Disable-NetFirewallRule -Name 'WINRM-HTTP-In-TCP-NoScope'"

:: Use temporary ps1 file to add "WINRM-HTTPS-In-TCP-NoScope" firewall rule with cyrillic description
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
New-NetFirewallRule -Name 'WINRM-HTTPS-In-TCP-NoScope' `
                    -DisplayName 'Windows Remote Management (HTTPS-In)' `
                    -Group '@FirewallAPI.dll,-30267' `
                    -Description 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5986]' `
                    -Profile Any `
                    -LocalPort 5986 `
                    -Protocol TCP
New-NetFirewallRule -Name 'WINRM-HTTPS-In-TCP-NoScope' `
                    -DisplayName 'Удаленное управление Windows (HTTPS - входящий трафик)' `
                    -Group '@FirewallAPI.dll,-30267' `
                    -Description 'Правило входящего трафика для удаленного управления Windows через WS-Management. [TCP 5986]' `
                    -Profile Any `
                    -LocalPort 5986 `
                    -Protocol TCP
# Disable HTTP port (optional)
Disable-NetFirewallRule -Name "WINRM-HTTP-In-TCP-NoScope"

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

### Linux
* https://gbe0.com/posts/linux/desktop/linux-powershell-remote-to-windows-with-docker/

```powershell
Install-Module -Name PSWSMan -Force
Install-WSMan

$cred = Get-Credential
Enter-PSSession -ComputerName my-computer -Credential $cred
```

##### pypsrp
* https://pypi.org/project/pypsrp/
* https://github.com/jborean93/pypsrp

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
# No encryption
client = Client(
    "host.domain.tld",
    ssl=False, encryption="never", auth="basic",
    username="vagrant", password=os.environ["AO_DEFAULT_VAGRANT_PASSWORD"]
)

stdout, stderr, rc = client.execute_cmd("cmd /c ver", encoding="1251")
client.copy("/path/to/script.ps1", 'c:\\temp\\script.ps1')
```

```powershell
# 2check
# https://github.com/jborean93/pypsrp/issues/94
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#[System.Text.Encoding]::Default
```


##### pywinrm
* https://pypi.org/project/pywinrm/
* https://github.com/diyan/pywinrm
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

### Unencrypted

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
