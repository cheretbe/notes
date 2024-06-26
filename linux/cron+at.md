* :point_right: Cron expression generator/validator: https://www.freeformatter.com/cron-expression-generator-quartz.html
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

* https://habilis.net/cronic/ - wrapper for sending mails on errors only
    * A fork that adds option to ignore stderr: https://github.com/dismantl/cronic 

### Debugging 

* https://gitlab.com/doctormo/python-crontab
* https://stackabuse.com/scheduling-jobs-with-python-crontab/

`/etc/cron.d/cron_test`
```
27 19 * * * root systemd-cat -t "cron_test" date -Iseconds
```
```shell
pip3 install python-crontab
```
```python
import datetime
import crontab

cron = crontab.CronTab(tabfile="/etc/cron.d/cron_test")

run_date = datetime.datetime.now()
inc_minutes = 1
if run_date.second > 55:
    inc_minutes = 2

run_date += datetime.timedelta(minutes=inc_minutes)

cron[0].minute.on(run_date.minute)
cron[0].hour.on(run_date.hour)
print(f"Date: {datetime.datetime.now()}, cron: {run_date.hour}:{run_date.minute}")

cron.write()
```

```shell
journalctl -u cron -f -n 0
```

### at command
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

# Reboot in ~5 minutes (at doesn't use seconds)
at $(date -d "today +5 min" +"%H:%M %Y-%m-%d") <<EOF
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

# Reboot tomorrow at 04:00
at $(date --date=tomorrow +"04:00 %Y-%m-%d") <<EOF
echo "\$(date) - Rebooting $(hostname -f)" \
   | mail $USER -s "Scheduled reboot of $(hostname -f)"
/sbin/reboot
EOF
```
