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

```shell
ansible win10 -m community.windows.win_credential \
  -a "name=name=host.domain.tld type=domain_password username=name=host.domain.tld\username secret=pwd" \
  --extra-vars "ansible_become=true ansible_become_method=runas ansible_become_user=vagrant ansible_become_pass=vagrant"

ansible win10 -m community.windows.win_credential -a "name=host.domain.tld type=domain_password state=absent" \
  --extra-vars "ansible_become=true ansible_become_method=runas ansible_become_user=vagrant ansible_become_pass=vagrant"
```
