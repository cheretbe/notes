`whiptail` is less powerful, but has an advantage of it's package being installed on most boxes by default

```bash
# The following swaps stdout and stderr
# 3>&1 - Create a file descriptor 3 and point to FD 1.
# 1>&2 - Redirect FD 1 to FD 2. If we wouldn't have saved the FD in 3 we would lose the target.
# 2>&3 - Redirect FD 2 to FD 3. Now FDs 1 and 2 are switched.
# 3>&- - Close FD 3
3>&1 1>&2 2>&3 3>&-
```
