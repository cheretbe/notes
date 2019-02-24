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
