## Table of Contents
* [Troubleshooting](#troubleshooting)
* [Submodules](#submodules)

###Troubleshooting
``` shell
# Increase verbosity
git 'command' --verbose
# or
git 'command' -v
# Also useful
git 'command' --dry-run
GIT_CURL_VERBOSE=1 git 'command'
GIT_TRACE_PACKET=2 git 'command'
# On Windows
SET GIT_CURL_VERBOSE=1
SET GIT_TRACE_PACKET=2
```
Make sure `--verbose` switch is **after the actual git command**, otherwise it won' t work!

###Submodules
``` shell
git submodule add https://url [dir\subdir]
```

Unsorted:

http://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule

git submodule add https://url [dir**/**subdir] '/' on windows also!
