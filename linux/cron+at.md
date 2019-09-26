* https://stackoverflow.com/questions/2366693/run-cron-job-only-if-it-isnt-already-running/33416116#33416116
* https://debian-handbook.info/browse/stable/sect.task-scheduling-cron-atd.html

```
# ------------------------------------------------------------------------------------
#┌───────────── min (0 - 59)
#│ ┌────────────── hour (0 - 23)
#│ │ ┌─────────────── day of month (1 - 31)
#│ │ │ ┌──────────────── month (1 - 12)
#│ │ │ │ ┌───────────────── day of week (0 - 6) (0 to 6 are Sunday to Saturday, or use names (Mon or Monday); 7 is Sunday, the same as 0)
#│ │ │ │ │
#│ │ │ │ │
#* * * * *  command to execute
# ------------------------------------------------------------------------------------
```
`at` command
```shell
echo /bin/systemctl daemon-reload | /usr/bin/at 09:00 27.07.15
at 09:00 27.07.15 <<EOF
echo "test" \
   | mail $USER -s "at command test"
EOF
# Postpone the execution for a given duration
# The period can be minutes, hours, days, or weeks
# at now + 1 hour
# at now + 3 days
at now + 1 min <<EOF
echo "test" \
   | mail $USER -s "at command test"
EOF

# List scheduled tasks
atq
# View details of a task
at -c <id>
# Delete a task
atrm <id>
# or
at -d <id>
```

```shell
# schedule a reboot
at 23:00 27.07.15 <<EOF
echo "\$(date) - Rebooting $(hostname -f)" \
   | mail $USER -s "Scheduled reboot of $(hostname -f)"
/sbin/reboot
EOF

# Reboot today at 23:00
at $(date +"23:00 %Y-%m-%d") <<EOF
echo "\$(date) - Rebooting $(hostname -f)" \
   | mail $USER -s "Scheduled reboot of $(hostname -f)"
/sbin/reboot
EOF
```
