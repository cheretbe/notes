* http://www.bahmanm.com/blogs/command-line-options-how-to-parse-in-bash-using-getopt
* https://github.com/ecoon/amanzi-columns/blob/master/tools/config/do-configure-netcdf
* https://github.com/boldleadsdevelopment/lockdown/blob/master/lib/determine_linux_distro
* http://hackaday.com/2017/07/21/linux-fu-better-bash-scripting/


Try adding the following to `~/.inputrc` file:
```
# Use [Tab] and [Shift]+[Tab] to cycle through all the possible completions:
"\t": menu-complete
"\e[Z": menu-complete-backward
set completion-ignore-case
```
(breaks Home/End buttons and does not enter into directores)


```bash
#!/bin/bash

search_dir="/path/to/a/dir"

for subdir in "$search_dir"/*
do
  if [ ! -h "$subdir" ]
  then
    echo "$subdir"
    #ls "$subdir/data/0000/"
    rm -R "$subdir/data/0000/"
  fi
done

while true; do echo "test line"; sleep 5; done;
while true
do
  echo "stdout test"
  sleep 3
  >&2 echo "stderr test"
  sleep 3
done

```

```bash
printf "Adding %s (%s) to /etc/hosts\n" ${other_host_name} ${other_host_ip}
```

### .bashrc File

```bash
# Alias
alias gs="git fetch && git status"
# Apply changes
source ~/.bashrc
```

### Options
#### Unofficial Strict Mode
```bash
# -e          Exit immediately if a command exits with a non-zero status
# -u          Treat unset variables as an error when substituting
# -o pipefail The return value of a pipeline is the status of
#             the last command to exit with a non-zero status,
#             or zero if no command exited with a non-zero status
set -euo pipefail
```
* http://redsymbol.net/articles/unofficial-bash-strict-mode/
#### Debug
* `set -x` or `set -o xtrace` expands variables and prints a little + sign before the line
* `set -v` or `set -o verbose` does not expand the variables before printing
* Use `set +x` and `set +v` to turn off the above settings

### If statement
The square brackets are a synonym for the test command. An if statement checks the exit status of a command in order to decide which branch to take. `grep -q "$text"` is a command, but `"$name" = 'Bob'` is not - it's just an expression.
* https://stackoverflow.com/questions/8934012/when-square-brackets-are-required-in-bash-if-statement/8934070#8934070
* https://stackoverflow.com/questions/3427872/whats-the-difference-between-and-in-bash/3427931#3427931

```bash
command1
if [ $? -ne 0 ]; then
    echo "command1 has failed"
fi

# Each command must be properly terminated, either by a newline or a semi-colon
if [ $? -ne 0 ] ; then echo 1; else echo 0 ; fi

if [ ! -f /path/to/file ]; then; echo "File not found!"; fi
```
#### Primary expressions
| Expression    | Meaning                                     |
|---------------|---------------------------------------------|
| `[ -a FILE ]` | True if `FILE` exists (deprecated according to [this](https://stackoverflow.com/a/321352)) |
| `[ -e FILE ]`	| True if `FILE` exists                       |
| `[ -f FILE ]`	| True if `FILE` exists and is a regular file |
| `[ -d FILE ]`	| True if `FILE` exists and is a directory    |

#### Combining expressions

| Operation            | Effect                                 |
|----------------------|----------------------------------------|
| `[ ! EXPR ]`         | True if EXPR is false                  |
| `[ ( EXPR ) ]`       | Returns the value of EXPR. This may be used to override the normal precedence of operators |
| `[ EXPR1 -a EXPR2 ]` |	True if both EXPR1 and EXPR2 are true |
| `[ EXPR1 -o EXPR2 ]` |	True if either EXPR1 or EXPR2 is true |

* http://www.gnu.org/software/bash/manual/bashref.html#Bash-Conditional-Expressions
* http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html
