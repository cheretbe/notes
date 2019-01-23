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
