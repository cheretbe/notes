`Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `System` > `Local Services`<br>
`Disallow copying of user input methods to the system account for sign-in` -> `Enabled`

`Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Административные шаблоны` >
`Система` > `Службы языковых стандартов`<br>
`Запретить копирование пользовательских методов ввода в системную учетную запись для входа` -> `Включено`

`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Control Panel\International`: BlockUserInputMethodsForSignIn = 1

---------------
https://github.com/cheretbe/notes/blob/master/windows/group_policies.md#installation-and-init
```powershell
Get-PolicyFileEntry -Path "${ENV:SystemRoot}\system32\GroupPolicy\Machine\Registry.pol" -All
```
```batch
gpupdate /force
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization /v NoLockScreen
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v EnableFirstLogonAnimation
reg query HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v ACSettingIndex
reg query HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v DCSettingIndex
```
---------------
* [ ] Disable the lock screen<br>
    `Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `Control Panel` > `Personalization`:<br>
    `Do not display the lock screen` -> `Enabled`<br>
    `Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Админстративные шаблоны` > `Панель управления` > `Персонализация`:<br>
    `Запрет отображения экрана блокировки` -> `Включено`<br>
    :point_right:
    ```powershell
    Set-PolicyFileEntry -Path "${ENV:SystemRoot}\system32\GroupPolicy\Machine\Registry.pol" `
      -Key "Software\Policies\Microsoft\Windows\Personalization" `
      -ValueName "NoLockScreen" -Type dword -Data 1
    ```


---------------
* [ ] Disable first sign-in animation<br>
    `Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `System` > `Logon`:<br>
    `Show first sign-in animation` -> `Disabled`<br>
    `Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Админстративные шаблоны` > `Система` > `Вход в систему`:<br>
    `Показать анимацию при первом входе в систему` -> `Отключено`<br>
    :point_right:
    ```powershell
    Set-PolicyFileEntry -Path "${ENV:SystemRoot}\system32\GroupPolicy\Machine\Registry.pol" `
      -Key "Software\Microsoft\Windows\CurrentVersion\Policies\System" `
      -ValueName "EnableFirstLogonAnimation" -Type dword -Data 0
    ```


---------------
* [ ] Disable password requirement when the computer wakes<br>
    `Computer Configuration` > `Administrative Templates` > `System` > `Power Management` > `Sleep Settings`:<br>
    `Require a Password when the computer wakes (plugged in)` -> `Disabled`<br>
    `Require a Password when the computer wakes (on battery)` -> `Disabled`<br>
    `Конфигурация компьютера` > `Административные шаблоны` > `Система` > `Управление электропитанием` > `Параметры спящего режима`:<br>
    `Требовать пароль при выходе из спящего режима (питание от сети)` -> `Отключено`<br>
    `Требовать пароль при выходе из спящего режима (питание от батареи)` -> `Отключено`<br>
    *Plugged in* :point_right: `reg add HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v ACSettingIndex /t REG_DWORD /d 0 /f`<br>
    *On battery* :point_right: `reg add HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v DCSettingIndex /t REG_DWORD /d 0 /f`
