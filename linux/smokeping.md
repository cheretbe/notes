```shell
# Smokeping targets
nano /etc/smokeping/config.d/Targets
service smokeping restart

# [!!!] when changing step (ping frequncy) parameter in /etc/smokeping/config.d/Probes
# see note on old RRD files deletion in https://oss.oetiker.ch/smokeping/probe/FPing.en.html
# By default RRD files are in `/var/lib/smokeping`

```

```
*** Targets ***

probe = FPing

menu = Top
title = Network Latency Grapher
remark = Welcome to the SmokePing website of xxx Company. \
         Here you will learn all about the latency of our network.

+ Local

menu = Local
title = Local Network
#parents = owner:/Test/James location:/

++ LocalMachine
menu = localhost
title = localhost
host = localhost
#alerts = someloss

++ Router
menu = 192.168.1.1 (router)
title = 192.168.1.1 (router)
host = 192.168.1.1

++ Some other local host
menu = 192.168.1.10 (local host)
title = 192.168.1.10 (local host)
host = 192.168.1.10


+ Remote
menu = Remote
title = Remote targets

++ 212_48_195_246
menu = 212.48.195.246 (remote gw)
title = 212.48.195.246 (remote gw)
host = 212.48.195.246

++ 87_250_250_242
menu = 87.250.250.242 (ya.ru)
title = 87.250.250.242 (ya.ru)
host = 87.250.250.242


++ 1_1_1_1
menu = 1.1.1.1
title = 1.1.1.1
host = 1.1.1.1

++ 8_8_8_8
menu = 8.8.8.8
title = 8.8.8.8
host = 8.8.8.8

```

URL: `http://smokeping.domain.tld/cgi-bin/smokeping.cgi`
