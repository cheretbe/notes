```shell
# Generate locales on Debian/Ubuntu
# It reads /etc/locale.gen and shows dialog to select locales to generate
# (uncommented items shown as selected, commented left unselected) and updates
# the file according to user selection. Then it runs locale-gen (which also reads
# /etc/locale.gen and generates uncommented locales)
dpkg-reconfigure locales
```
Default locale config is in `/etc/default/locale`. Custom combination of parameters example:
```
LANG="en_US.UTF-8"
LANGUAGE="en_US:en"
LC_NUMERIC="ru_RU.UTF-8"
LC_TIME="ru_RU.UTF-8"
LC_MONETARY="ru_RU.UTF-8"
LC_PAPER="ru_RU.UTF-8"
LC_NAME="ru_RU.UTF-8"
LC_ADDRESS="ru_RU.UTF-8"
LC_TELEPHONE="ru_RU.UTF-8"
LC_MEASUREMENT="ru_RU.UTF-8"
LC_IDENTIFICATION="ru_RU.UTF-8"
```
