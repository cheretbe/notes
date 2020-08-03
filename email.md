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

```shell
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

### Configure Postfix to use Gmail as a Mail Relay

* https://www.howtoforge.com/tutorial/configure-postfix-to-use-gmail-as-a-mail-relay/

:warning: Enable "Less Secure Apps" In Gmail. Double check if it's on, since Google turns this feature off after awhile if it not being used.

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
