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

