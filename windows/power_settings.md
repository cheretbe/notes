* https://www.tenforums.com/tutorials/6039-choose-power-plan-context-menu-add-windows-10-a.html


Active power scheme:<br>
`HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Power\User\Default\PowerSchemes` > `ActivePowerScheme`
```batch
powercfg /GETACTIVESCHEME
```

```batch
:: Shows all GUIDs with values and descriptions in hierarchical order
powercfg /QUERY
powercfg /QUERY 381b4222-f694-41f0-9685-ff5bb260df2e
```


:warning: 2arrange similar to items in installation checklist:
```
Управление электропитанием Параметры спящего режима

Указать время ожидания автоматического перехода в спящий режим (питание от сети)
Software\Policies\Microsoft\Power\PowerSettings\7bc4a2f9-d8fc-4469-b07b-33eb785aaca0 ACSettingIndex

Укажите время ожидания автоматического перехода в спящий режим (питание от батареи)
Software\Policies\Microsoft\Power\PowerSettings\7bc4a2f9-d8fc-4469-b07b-33eb785aaca0 DCSettingIndex


Управление электропитанием Параметры дисплея и видео

Отключить дисплей (питание от сети)
Software\Policies\Microsoft\Power\PowerSettings\3C0BC021-C8A8-4E07-A973-6B14CBCB2B7E ACSettingIndex

Отключить дисплей (питание от батареи)
Software\Policies\Microsoft\Power\PowerSettings\3C0BC021-C8A8-4E07-A973-6B14CBCB2B7E DCSettingIndex


reg add HKLM\Software\Policies\Microsoft\Power\PowerSettings\3C0BC021-C8A8-4E07-A973-6B14CBCB2B7E /v DCSettingIndex /t REG_DWORD /d 10 /f
```
