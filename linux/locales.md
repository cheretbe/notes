* https://wiki.debian.org/Locale
    * Supported locales are in `/usr/share/i18n/SUPPORTED`
    * `LANG` contain the setting for all categories that are not directly set by a `LC_*` variable
    * `LANGUAGE` is used to set messages languages (as `LC_MESSAGES`) to a multi-valued value, e.g., setting it to `fr:de:en` will use French messages where they exist; if not, it will use German messages, and will fall back to English if neither German nor French messages are available.

```shell
# Get locale-specific information
locale
# or
localectl status


# Generate locales on Debian/Ubuntu
# It reads /etc/locale.gen and shows dialog to select locales to generate
# (uncommented items shown as selected, commented left unselected) and updates
# the file according to user selection. Then it runs locale-gen (which also reads
# /etc/locale.gen and generates uncommented locales)
dpkg-reconfigure locales

# Verify the list of available locales
locale -a
# or
localectl list-locales
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
