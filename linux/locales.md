* https://wiki.debian.org/Locale
    * Supported locales are in `/usr/share/i18n/SUPPORTED`
    * `LANG` contain the setting for all categories that are not directly set by a `LC_*` variable
    * `LANGUAGE` is used to set messages languages (as `LC_MESSAGES`) to a multi-valued value, e.g., setting it to `fr:de:en` will use French messages where they exist; if not, it will use German messages, and will fall back to English if neither German nor French messages are available.
* RHEL
   * How to change system locale on RHEL7? https://access.redhat.com/solutions/974273
   * SYSTEM LOCALE AND KEYBOARD CONFIGURATION https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-keyboard_configuration

```shell
# Get locale-specific information
locale
# or
localectl status

# View more information about specific variable
locale -k LC_TIME


# Generate locales on Debian/Ubuntu
# It reads /etc/locale.gen and shows dialog to select locales to generate
# (uncommented items shown as selected, commented left unselected) and updates
# the file according to user selection. Then it runs locale-gen (which also reads
# /etc/locale.gen and generates uncommented locales)
dpkg-reconfigure locales

# Generate locales on RHEL 7/8
# On RHEL 8 make sure glibc-locale-source package is installed
yum install glibc-locale-source
localedef -c -i ru_RU -f UTF-8 ru_RU.UTF-8

# Docker container centos:7 used to have a problem when generating locales. See
# https://blog.nashcom.de/nashcomblog.nsf/dx/locale-issue-on-linux-centos-rhel.htm
# https://serverfault.com/questions/616790/how-to-add-language-support-on-centos-7-on-docker/884562#884562
# /etc/yum.conf contains the line 'override_install_langs=en_US'. This causes yum reinstall glibc-common to
# only install English. As of December 2020 /etc/yum.conf still contains the option, but localedef no longer
# fails. Just make sure that 'initscripts' package is installed

# Verify the list of available locales
locale -a
# or
localectl list-locales
# They are located in /usr/lib/locale/locale-archive file
ls -lha /usr/lib/locale/locale-archive

# Set system locale
localectl set-locale LANG=ru_RU.UTF-8
localectl set-locale LANG=en_US.UTF-8 LC_TIME=ru_RU.UTF-8

# Ubuntu also has update-locale script
# Does the same, but can unset (comment out) existing parameters like this
update-locale LANG=ru_RU.UTF-8 LANGUAGE LC_TIME
```

System locale config is in `/etc/default/locale` (Debian/Ubuntu) or `/etc/locale.conf` (RHEL/CentOS). Custom combination of parameters example:
```
LANG="en_US.UTF-8"
# LANGUAGE="en_US:en"
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

### Localization (2check)

```shell
# RHEL 8
yum list installed langpacks*
yum list langpacks-*
yum install langpacks-ru
```
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_basic_system_settings/using-langpacks_configuring-basic-system-settings
