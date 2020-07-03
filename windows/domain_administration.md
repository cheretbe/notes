* https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-#BKMK_PS
* https://sid-500.com/2017/07/01/powershell-how-to-install-a-domain-controller-with-server-core/
* https://www.ansible.com/blog/active-directory-ansible-tower
* https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html

Create an OU
```powershell
# New-ADOrganizationalUnit doesn't support parent creation
# So, to create nested OUs '/level1/level2/level3' in 'dummy.local' domain,
# the following commands are needed
New-ADOrganizationalUnit -Name 'level1' -Path 'DC=dummy,DC=local'
New-ADOrganizationalUnit -Name 'level2' -Path 'OU=level1,DC=dummy,DC=local'
New-ADOrganizationalUnit -Name 'level3' -Path 'OU=level2,OU=level1,DC=dummy,DC=local'
```
