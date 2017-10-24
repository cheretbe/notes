* https://stackoverflow.com/questions/2366693/run-cron-job-only-if-it-isnt-already-running/33416116#33416116

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
