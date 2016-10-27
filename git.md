## Table of Contents
* [Troubleshooting](#troubleshooting)
* [Submodules](#submodules)
* [Unsorted](#unsorted)

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
Make sure `--verbose` switch is **after the actual git command**, otherwise it won't work!

###Submodules
``` shell
# Add submbodule
# [!] No trailing slash or command will fail
# [!] Use '/' even on Windows. If '\' is used, the command itself will not fail, but later updates will
git submodule add https://url [dir/subdir]
# View status
git submodule status
# Clone a repository and download submodules simultaneously
git clone --recursive https://url
# Download submodules in an already cloned repository
git submodule update --init --recursive
```
Submodules always point to a specific commit in the linked repository.

###Unsorted

http://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule

git submodule add https://url [dir**/**subdir] '/' on windows also!
