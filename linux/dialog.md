`whiptail` is less powerful, but has an advantage of its package being installed on most boxes by default

* https://github.com/Archivists/ltfs-console/tree/master/samples
* https://bash.cyberciti.biz/guide/Main_Page
    * Chapter 10: Interactive Scripts > Bash display dialog boxes

```bash
# The following swaps stdout and stderr
# 3>&1 - Create a file descriptor 3 and point to FD 1.
# 1>&2 - Redirect FD 1 to FD 2. If we wouldn't have saved the FD in 3 we would lose the target.
# 2>&3 - Redirect FD 2 to FD 3. Now FDs 1 and 2 are switched.
# 3>&- - Close FD 3
3>&1 1>&2 2>&3 3>&-
```
```bash
# By default dialog returns 255 on ESC. It gets mixed up with error code -1
# converted to unsigned 8-bit. We set DIALOG_ESC variable to use the same
# code as Cancel since we don't need to distinguish ESC and Cancel.
result=$(DIALOG_ESC=1 dialog --keep-tite --title "window title" \
  --form "form name" 0 0 0 \
  "item 1" 1 1 "default1" 1 15 10 0 \
  "item 2" 2 1 "default2" 2 15 10 0 \
  3>&1 1>&2 2>&3 3>&-); echo $?; printf "$result\n"
  
result=$(DIALOG_ESC=1 dialog --keep-tite --title "window title" \
  --default-item 2 \
  --menu "Select an item" 0 0 0 \
  1 "item 1" \
  2 "item 2" \
  3 "item 3" \
  3>&1 1>&2 2>&3 3>&-); echo $?; printf "$result\n"

```
