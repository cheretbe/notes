* https://blog.woodpecker.co/cold-email/reputation-domain-ip/
* https://www.mail-tester.com/
* https://ismyemailworking.com/AdvancedTest/
* https://analyze.email/
* https://fraudguard.io/
* https://blog.rebrandly.com/domain-reputation-links/
* https://www.spamhaus.org/statistics/tlds/
----
* https://hostripples.com/business-email.php
* https://www.hostinger.ru/poctovij-hosting
* https://www.mailcheap.co/email-shared.html
* https://www.servermx.com/en/index.html
* https://www.zoho.com/mail/
----

```shell
# For mail command to be available install corresponding package
apt install mailutils
yum install mailx
# Test default MTA mail delivery ('mailutils' package needs to be installed)
echo test | mail -s "test mail" root
echo test | mail -s "test mail" user@lan.domain.tld

echo "Message test" | mailx -v -r "someone@example.com" \
  -s "Test subject" -S smtp="mail.example.com:587" \
  -S smtp-use-starttls -S smtp-auth=login -S ssl-verify=ignore \
  -S smtp-auth-user="someone@example.com" -S smtp-auth-password="abc123" yourfriend@gmail.com
```
Testing POP3 with telnet
```
telnet mail.my-mail-server.com 110
user email@my-best-domain.com
pass my-password
quit
```

### Postfix

* http://www.postfix.org/postconf.1.html
* http://www.postfix.org/postconf.5.html
* http://www.postfix.org/BASIC_CONFIGURATION_README.html
* http://www.postfix.org/STANDARD_CONFIGURATION_README.html
* Setup a Local Only SMTP Email Server: https://gist.github.com/raelgc/6031274
* https://serverfault.com/questions/94168/postfix-on-development-server-allow-mail-to-be-sent-to-only-one-domain
* http://cubicspot.blogspot.com/2015/01/quick-n-dirty-postfix-and-dovecot-setup.html
* https://serverfault.com/questions/639615/postfix-and-local-mail/639694#639694
* :warning: Debconf peculiarity: https://serverfault.com/questions/889438/dpkg-reconfigure-dialog-frontend-sets-up-postfix-successfully-non-interactive/914012#914012
* http://cafim.sssup.it/~giulio/other/Postfix_Setup_for_Local_Mail_Only.html

:warning: Install on Ubuntu using the following command
```shell
DEBIAN_PRIORITY=low apt install postfix
```
Without low priority dialogs turned on debconf doesn't ask for root alias and writes `/etc/aliases` without it.
`dpkg-reconfigure postfix` does ask for additional settings, but doesn't actually set them, since `/etc/aliases`
and `/etc/postfix/main.cf` already present (and config script doesn't overwrite or edit these files).


```shell
# View version
postconf mail_version
# View configuration
postconf

# View only configuration parameters that have explicit name=value settings in main.cf
postconf -n
# View single parameter value
postconf smtpd_use_tls
# View settings that differ from built-in defaults
comm -23 <(postconf -n | sort) <(postconf -d | sort)
# View settings that duplicate built-in defaults
comm -12 <(postconf -n | sort) <(postconf -d | sort)
# [!] To view settings that differ from built-in defaults alongside with their default
# values use python code below

# View all default values
postconf -d
# View default value for a parameter
# -h shows value without the "name = " prefix
postconf -d -h smtpd_use_tls

# Change parameters
# The form [hostname] turns off MX lookups. Multiple destinations are supported in Postfix 3.5 and later.
postconf -e relayhost=[host.domain.tld]

# Check and apply new settings
postfix check
systemctl restart postfix
```

View settings that differ from built-in defaults alongside with their default values
```python
import subprocess

for line in sorted(subprocess.check_output(["postconf", "-n"], universal_newlines=True).splitlines()):
    param, value = [x.strip() for x in line.split("=", 1)]
    default_value = subprocess.check_output(
        ["postconf", "-d", "-h", param], universal_newlines=True
    ).strip("\n")
    if value != default_value:
        print(f"{param} = {value} [{default_value}]")
```

* `smtp_tls_security_level`: The default SMTP TLS security level for the Postfix SMTP **client**
* `smtpd_tls_security_level`: The SMTP TLS security level for the Postfix SMTP **server**
* `smtpd_use_tls`: Opportunistic TLS: announce STARTTLS support to remote SMTP clients, but do not require that clients use TLS encryption.
                   With Postfix 2.3 and later use `smtpd_tls_security_level` instead.

### Configure Postfix to use Gmail as a Mail Relay

* https://www.howtoforge.com/tutorial/configure-postfix-to-use-gmail-as-a-mail-relay/

:warning: Enable "Less Secure Apps" In Gmail. Double check if it's on, since Google turns this feature off after awhile if it's not being used.

```shell
# select "no configuration"
apt install postfix mailutils

nano /etc/postfix/sasl_passwd
```

```
[smtp.gmail.com]:587    username@gmail.com:password
```

```shell
chmod 600 /etc/postfix/sasl_passwd

nano /etc/postfix/main.cf
```
The host is enclosed in brackets to specify that no MX lookup is required.
```
relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_security_options =
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```

```shell
postmap /etc/postfix/sasl_passwd
service postfix restart
echo test | mail -s "test mail" user@domain.tld
```

## Testing
#### MailHog is an email testing tool for developers
:warning: has REST API
* https://github.com/mailhog/MailHog
* https://jfelix.info/blog/test-your-email-flow-with-mailhog-a-fake-smtp-server


#### smtp4dev - the fake SMTP email server for development and testing

* https://github.com/rnwood/smtp4dev

```shell
# Download zip file from https://github.com/rnwood/smtp4dev/releases
# [!!] Make sure you are downloading 'linux-x64' package and not 'linux-musl-x64' one
# zip file doesn't contain a subdirectory, so use -d option
unzip -d smtp4dev Rnwood.Smtp4dev-linux-x64-3.1.2-ci20201203102.zip
# Run as root to be able to bind to privileged (<1024) ports
./Rnwood.Smtp4dev --urls "http://0.0.0.0:80/"
# Running as root should be okay for development tests, but if it
# not, add CAP_NET_BIND_SERVICE capability using setcap
sudo setcap 'cap_net_bind_service=+ep' /path/to/Rnwood.Smtp4dev
```
