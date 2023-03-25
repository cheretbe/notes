* http://www.bahmanm.com/blogs/command-line-options-how-to-parse-in-bash-using-getopt
* https://github.com/ecoon/amanzi-columns/blob/master/tools/config/do-configure-netcdf
* https://github.com/boldleadsdevelopment/lockdown/blob/master/lib/determine_linux_distro
* http://hackaday.com/2017/07/21/linux-fu-better-bash-scripting/

```shell
# ping targets from a file
readarray -t targets < temp/ping_targets.txt; for target in "${targets[@]}"; do ping -c1 "${target}"; done
# Show ping results only
readarray -t targets < temp/ping_targets.txt; for target in "${targets[@]}"; do ping -c1 "${target}" > /dev/null && echo "${target} is UP" || echo "${target} is down"; done

cat requests_log.txt| awk '{print $1}' | sort | uniq
```

```shell
echo "HISTCONTROL=ignoreboth:erasedups" >>~/.bashrc
```


Try adding the following to `~/.inputrc` file:
```
# Use [Tab] and [Shift]+[Tab] to cycle through all the possible completions:
"\t": menu-complete
"\e[Z": menu-complete-backward
set completion-ignore-case
```
(breaks Home/End buttons and does not enter into directores)


```bash
grep -qxF '. ~/.cache/venv/ansible-venv/bin/activate' /home/vagrant/.bashrc || echo -e '\\n. ~/.cache/venv/ansible-venv/bin/activate\\n' >>/home/vagrant/.bashrc

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

# -z switch tests if the expansion of "$1" is a null string or not
if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi

if ! command -v ansible --version &> /dev/null
then
  >&2 echo "Anbsile could not be found. Make sure the script is executed in a proper virtualenv"
  exit 1
fi

# Yes/No question with default yes
read -p "Do you want to continue? [Y/n] " -r
if [[ ! $REPLY =~ ^([yY][eE][sS]|[yY]|)$ ]]; then exit 1 ; fi

echo "Waiting for SSH to become available"
timeout 1m bash -c 'until ssh root@mynewvm; do sleep 10; done'
if [ $? -ne 0 ]; then
    >&2 echo "Timeout waiting for SSH to become available"
    exit 1
fi

# include (as equivalent for 'source' for future searches :))
# older version
# if [ "${BASH_SOURCE[0]}" -ef "$0" ]; then
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced/28776166#28776166
if ! (return 0 2>/dev/null); then
  echo >&2 "ERROR: This script needs to be sourced to run correctly"
  exit 1
fi
some_command
# [!!] Don't use 'exit' in a sourced script, use 'return' instead
if [ $? -ne 0 ]; then
  echo >&2 "ERROR: some_command execution has failed"
  return
fi

```

```bash
#!/bin/bash

# Get script path
script_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set test to a variable without echoing it
read -s -p "Password: " my_pwd; echo ""
# Optional export to expose the var to other processes
read -s -p "Password: " my_pwd; echo ""; export my_pwd

# Correct way (works with "set -euo")
# https://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-bash/13864829#13864829
if [ -z ${1+x} ]; then
# if [ -z "$1" ]; then
  echo "No argument supplied"
  exit 1
fi

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
echo "$(date -Iseconds) line with current timestamp"
echo "Custom-formatted current date: $(date +'%Y-%m-%d')"
```

```bash
until [ "`docker inspect -f {{.State.Health.Status}} gitlab`" == "healthy" ]; do echo "Waiting for container..."; sleep 2; done;
while [ ! -S /var/snap/lxd/common/lxd/unix.socket ]; do echo "Waiting for LXD socket..."; sleep 0.2; done;

# retry 5 times
# A subshell is used to keep $max out of the current shell
(max=5; for n in `seq 1 $max`; do your_command && break; done)
# or just
for n in `seq 1 5`; do your_command && break; done

echo "Waiting for AWX web interface to become available"
SECONDS=0
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:80)" -ne "200" ]]; do
    if [ $SECONDS -gt 300 ]; then
      >&2 echo "ERROR: Timeout waiting for AWX web interface (300s)"
      exit 1
    fi
    sleep 5
done
echo "Done"
```

### .bashrc File

```bash
# Alias
alias gs="git fetch && git status"
# Apply changes
source ~/.bashrc
```

### Here documents (heredocs) with indentation

```bash
# no indentation
cat > /path/to/newFile.text<< EOF
some text line 1
some text line 2
some text line 3
EOF
```

```bash
# [!!!!] Heredocs part MUST be tab-indented for <<-EOF part to work
# Sublime Text setting: "translate_tabs_to_spaces": false
if [ ! -e "/etc/ppp/pppoe-server-options" ]; then
	echo "Creating '/etc/ppp/pppoe-server-options'"
	cat <<-EOF > /etc/ppp/pppoe-server-options
		auth
		require-chap
		lcp-echo-interval 10
		lcp-echo-failure 2
		# DNS servers that our pppoe server will serve to clients 
		ms-dns ${pppoe_dns_1}
		ms-dns ${pppoe_dns_2}
		noipdefault
		noipx
		nodefaultroute
		noproxyarp
		# Netmask that clients will receive
		netmask 255.255.255.255
		logfile /var/log/pppoe.log
	EOF
fi
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

if [ $? -ne 0 ]
then
      echo 1
else
      echo 0
fi

# Negation
if [ ! -f /path/to/file ]; then echo "File not found!"; fi
```
#### Primary expressions
| Expression        | Meaning                                     |
|-------------------|---------------------------------------------|
| `[ -a FILE ]`     | True if `FILE` exists (deprecated according to [this](https://stackoverflow.com/a/321352)) |
| `[ -e FILE ]`	    | True if `FILE` exists                       |
| `[ -f FILE ]`	    | True if `FILE` exists and is a regular file |
| `[ -d FILE ]`	    | True if `FILE` exists and is a directory    |
| `[ -z "${var}" ]` | True if variable is unset or empty          |
| `[ -z ${var+x} ]` | True if variable is unset (:warning: use this on rare occasions where it matters) |

#### Combining expressions

| Operation            | Effect                                 |
|----------------------|----------------------------------------|
| `[ ! EXPR ]`         | True if EXPR is false                  |
| `[ ( EXPR ) ]`       | Returns the value of EXPR. This may be used to override the normal precedence of operators |
| `[ EXPR1 -a EXPR2 ]` |	True if both EXPR1 and EXPR2 are true |
| `[ EXPR1 -o EXPR2 ]` |	True if either EXPR1 or EXPR2 is true |

* http://www.gnu.org/software/bash/manual/bashref.html#Bash-Conditional-Expressions
* http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html
