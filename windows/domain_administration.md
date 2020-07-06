* https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-#BKMK_PS
* https://sid-500.com/2017/07/01/powershell-how-to-install-a-domain-controller-with-server-core/
* https://www.ansible.com/blog/active-directory-ansible-tower
* https://docs.ansible.com/ansible/latest/modules/list_of_windows_modules.html

To be able to delete protected objects in `Active Directory Users and Computers` snap-in, select
`View` > `Advanced Features`. This shows (among other things) `Protect object from accidental deletion`
option in `Object` tab.

Create an OU
```powershell
# New-ADOrganizationalUnit doesn't support parent creation
# So, to create nested OUs '/level1/level2/level3' in 'dummy.local' domain,
# the following commands are needed
New-ADOrganizationalUnit -Name 'level1' -Path 'DC=dummy,DC=local'
New-ADOrganizationalUnit -Name 'level2' -Path 'OU=level1,DC=dummy,DC=local'
New-ADOrganizationalUnit -Name 'level3' -Path 'OU=level2,OU=level1,DC=dummy,DC=local'
```

##### Avoid registering unwanted NIC(s) in DNS on a Mulithomed Domain Controller
Original link: https://support.microsoft.com/en-us/help/2023004/steps-to-avoid-registering-unwanted-nic-s-in-dns-on-a-mulithomed-domai

Extract (in case the link dies):<br>
To avoid this problem perform the following 3 steps (It is important that you follow all the steps to avoid the issue).
1. Under Network Connections Properties:
On the Unwanted NIC `TCP/IP Properties` > `Advanced` > `DNS` > Uncheck `Register this connections Address in DNS`

2. Open the DNS server console:  highlight the server on the left pane `Action` > `Properties` and on the `Interfaces` tab select `listen on only the following IP addresses`. Remove unwanted IP address from the list

3. On the Zone properties, select `Name` server tab. Along with FQDN of the DC, you will see the IP address associated with the DC. Remove unwanted IP address if it is listed.

After performing this delete the existing unwanted Host A record of the DC.
