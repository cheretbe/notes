* The most concise and reasonable summary: https://elims.org.ua/blog/nastraivaem-ntp/
* https://github.com/saltstack/salt/blob/master/salt/modules/win_ntp.py
* Ansible (not implemented)
    * https://github.com/ansible-collections/community.windows/issues/114
    * https://github.com/ansible-collections/community.windows/pull/150

```batch
:: /manualpeerlist:"server,0x0X" meaning:
::   https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-sntp/fef409e4-5297-4f18-850b-e386f7e10fea
::   The "Bitwise Flag", if included, MUST be a bitwise OR of zero or more of the following flags
::   0x01 SpecialInterval: The value of the SpecialPollInterval element is used as the polling interval for this time source.
::   0x02 UseAsFallbackOnly: Use this time source only when all other time sources have failed. No preference is given among fallback time sources when multiple time sources are configured with this option.
::   0x04 SymmetricActive: Use the symmetric active mode when communicating with this time source.
::   0x08 Client: Use the client mode when communicating with this time source.
::  So, 0x09 will mean SpecialInterval+Client

w32tm /query /configuration
w32tm /query /peers

w32tm /config /manualpeerlist:"0.ru.pool.ntp.org,0x08 1.ru.pool.ntp.org,0x08" /syncfromflags:manual /reliable:yes /update
:: Looks like service restart isn't needed (/update takes care of that), but sometimes service
:: isn't running add needs to be started
net stop w32time
net start w32time
w32tm /resync /rediscover

:: Debugging
w32tm /debug /enable /file:C:\temp\w32time_log.txt /size:100000 /entries:0-300
w32tm /debug /disable
```
