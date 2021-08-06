```batch
:: See which group policies are applied to your PC and user account
rsop.msc

:: View all the policies applied to the user account you’re currently logged in with
gpresult /Scope User /v

:: View all the policies applied to your computer
gpresult /Scope Computer /v

gpedit.msc

gpupdate /force
```
* https://www.howtogeek.com/116184/how-to-see-which-group-policies-are-applied-to-your-pc-and-user-account/
