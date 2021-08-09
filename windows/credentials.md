* `Control Panel` > `User Accounts and Family Safety` > `Credential Manager`
* `Панель управления` > `Учетные записи пользователей` > `Диспетчер учетных данных`

```batch
control /name Microsoft.CredentialManager
rundll32.exe keymgr.dll,KRShowKeyMgr

cmdkey /add:host.domain.tld /user:host.domain.tld\username /password:""
cmdkey /list
cmdkey /delete:host.domain.tld

VaultCmd /listcreds:"Windows Credentials"
VaultCmd /listcreds:"Учетные данные Windows"

:: List valid credential types
VaultCmd /listschema

VaultCmd /addcreds:"Windows Credentials" /credtype:"Windows Domain Password Credential" /identity:"host.domain.tld\username" /authenticator:"password" /resource:"host.domain.tld"
VaultCmd /addcreds:"Учетные данные Windows" /credtype:"Учетные данные пароля домена Windows" /identity:"host.domain.tld\username" /authenticator:"password" /resource:"host.domain.tld"

VaultCmd /deletecreds:"Windows Credentials" /credtype:"Windows Domain Password Credential" /identity:"host.domain.tld\username" /resource:"host.domain.tld"
VaultCmd /deletecreds:"Учетные данные Windows" /credtype:"Учетные данные пароля домена Windows" /identity:"host.domain.tld\username" /resource:"host.domain.tld"
```

* https://github.com/davotronic5000/PowerShell_Credential_Manager
```powershell
Install-Module CredentialManager

[enum]::GetValues([PSCredentialManager.Common.Enum.CredType])
[enum]::GetValues([PSCredentialManager.Common.Enum.CredPersist])

New-StoredCredential -Target "host.domain.tld" -Type DomainPassword -UserName "host.domain.tld\username" -Password "password" -Persist "LocalMachine"

Get-StoredCredential -AsCredentialObject
Get-StoredCredential -Type DomainPassword -AsCredentialObject -Target 'Domain:target=host.domain.tld'

# [!!!] It doesn't support pipelining, use ForEach-Object
Get-StoredCredential -Type DomainPassword -AsCredentialObject -Target 'Domain:target=host.domain.tld' | ForEach-Object { Remove-StoredCredential -Type DomainPassword -Target $_.TargetName }
```

```shell
ansible win10 -m community.windows.win_credential \
  -a "name=name=host.domain.tld type=domain_password username=name=host.domain.tld\username secret=pwd" \
  --extra-vars "ansible_become=true ansible_become_method=runas ansible_become_user=vagrant ansible_become_pass=vagrant"

ansible win10 -m community.windows.win_credential -a "name=host.domain.tld type=domain_password state=absent" \
  --extra-vars "ansible_become=true ansible_become_method=runas ansible_become_user=vagrant ansible_become_pass=vagrant"
```
