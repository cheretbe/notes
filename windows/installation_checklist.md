`Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `System` > `Local Services`<br>
`Disallow copying of user input methods to the system account for sign-in` -> `Enabled`

`Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Административные шаблоны` >
`Система` > `Службы языковых стандартов`<br>
`Запретить копирование пользовательских методов ввода в системную учетную запись для входа` -> `Включено`

`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Control Panel\International`: BlockUserInputMethodsForSignIn = 1

---------------
* [ ] Disable the lock screen<br>
    `Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `Control Panel` > `Personalization`:<br>
    `Do not display the lock screen` -> `Enabled`<br>
    `Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Админстративные шаблоны` > `Панель управления` > `Персонализация`:<br>
    `Запрет отображения экрана блокировки` -> `Включено`<br>
    :clipboard: `reg add HKLM\SOFTWARE\Policies\Microsoft\Windows\Personalization /v NoLockScreen /t REG_DWORD /d 1 /f`

---------------
* [ ] Disable first sign-in animation<br>
    `Local Group Policy` > `Computer Configuration` > `Administrative Templates` > `System` > `Logon`:<br>
    `Show first sign-in animation` -> `Disabled`<br>
    `Политика "Локальный компьютер"` > `Конфигурация компьютера` > `Админстративные шаблоны` > `Система` > `Вход в систему`:<br>
    `Показать анимацию при первом входе в систему` -> `Выключено`

---------------
* [ ] Disable password requirement when the computer wakes<br>
    `Computer Configuration` > `Administrative Templates` > `System` > `Power Management` > `Sleep Settings`:<br>
    `Require a Password when the computer wakes (plugged in)` -> `Disabled`<br>
    `Require a Password when the computer wakes (on battery)` -> `Disabled`<br>
    ~*Plugged in*~ :point_right: `reg add HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v ACSettingIndex /t REG_DWORD /d 0 /f`<br>
    ~*On battery*~ :point_right: `reg add HKLM\Software\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51 /v DCSettingIndex /t REG_DWORD /d 0 /f`
