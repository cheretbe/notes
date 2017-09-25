## Table of Contents
* [Unsorted](#unsorted)
* [Cheat Sheet](#cheat-sheet)
* [Initial setup](#initial-setup)
* [Troubleshooting](#troubleshooting)
* [Submodules](#submodules)
* [Branches and tags](#branches-and-tags)
* [Github backup](#github-backup)

### Unsorted
``` shell
# work with a different path instead of current working directory
git --git-dir /path/to/repo/.git --work-tree /path/to/repo status
```

### Cheat Sheet
```shell
# View config
git config [--global] –list

# Add all files recursively
git add .

# Undo add
git reset

# Rename file
git mv file new-name

# Delete file
git rm file.txt

# Delete, but leave it in the local filesystem:
git rm --cached file.txt

# Remove already deleted files from index:
git add -u .

# View commit history:
git log [-2] [--stat]

# Reuse previous commit message
git commit -c HEAD

# Revert changes to tracked files:
git reset –-hard

# Diff with previous commit
git diff HEAD^ HEAD
# On Windows use ~ unstead of ^
git diff HEAD~ HEAD
```

### Initial setup
```bash
git config --global user.name "user name"
git config --global user.email "email"
# Not needed in recent versions?
git config --global credential.helper wincred
# Linux (warning: stores in plaintext!):
git config --global credential.helper store
git config --global push.default simple
```

### Troubleshooting
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

### Submodules
``` shell
# Add submbodule
# [!] No trailing slash or command will fail
# [!] Use '/' even on Windows. If '\' is used, the command itself will not fail, but later updates will
git submodule add https://url [dir/subdir]
# View status
git submodule status
# Clone a repository and download submodules simultaneously
git clone --recursive https://url
# Download submodules in an already cloned repository (or if a submodule has been added later)
git submodule update --init --recursive

# Changing submodule URL
# Edit .gitmodules file
# Then run resync
git submodule sync
```
Specifying a branch/tag
``` shell
cd /path/to/yoursubmodule
git checkout yourTag
cd ..
# [!] Here we actually store the specific commit in our repository
git add /path/to/yoursubmodule
git commit -m "use submoduile at tag xx"
git push
# On another copy of the repo (after pull)
git submodule update --init --recursive
```
Submodules always point to a specific commit in the linked repository. To track a branch `-b` option can be used. Submodule will still point to some specific commit, but it can be updated to the latest commit with the following command:
``` shell
git submodule update --remote
```
http://stackoverflow.com/questions/1777854/git-submodules-specify-a-branch-tag/1778247#1778247

Deleting a submodule

http://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule/21211232#21211232
### Branches and tags

``` shell
# Merge back develop -> master and tag a version
# Make sure you are on master branch
git branch
# If not switch to it
git checkout master
# Merge (--no-ff skips "fast-forward")
git merge develop --no-ff
# Add a tag
git tag -a 1.0 -m "version 1.0"
git push --follow-tags
# View current tag
git describe --abbrev=0 --tags
# Switch back to develop
git checkout develop
```
### Github backup
http://github-backup.branchable.com/
```
# Check if gcc is actually needed
sudo apt install haskell-stack gcc zlib1g-dev libstdc++-5-dev g++
stack upgrade
/home/<user>/.local/bin/stack install --install-ghc
```
