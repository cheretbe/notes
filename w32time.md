```
w32tm /monitor /computers:0.pool.ntp.org
w32tm /query /source
w32tm /stripchart /computer:de.pool.ntp.org /samples:5 /dataonly
```
* https://www.experts-exchange.com/questions/28931427/W32time-still-using-local-CMOS-clock-after-NTP-client-setup.html
