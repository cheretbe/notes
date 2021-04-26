## Table of Contents
* [Unsorted](#unsorted)
* [Cheat Sheet](#cheat-sheet)
* [Initial setup](#initial-setup)
* [Troubleshooting](#troubleshooting)
* [Submodules](#submodules)
* [Branches and tags](#branches-and-tags)
* [Github backup](#github-backup)
* [.gitattributes Files](#gitattributes-files)

### Unsorted

Github
```shell
# Get latest release
release_data=$(curl -s https://api.github.com/repos/backuppc/backuppc-xs/releases/latest)
backuppc_xs_ver=$(echo ${release_data} | jq -r ".tag_name")
backuppc_xs_tar=$(echo ${release_data} | jq -r ".assets[0].name")
wget $(echo ${release_data} | jq -r ".assets[0].browser_download_url")
tar -xzvf ${backuppc_xs_tar}
cd BackupPC-XS-${backuppc_xs_ver}

# View current requests rate limits:
curl -i -u cheretbe:${GITHUB_OAUTH_TOKEN} https://api.github.com/users/cheretbe
# Non-authenticated (per IP):
curl -i https://api.github.com/rate_limit

# Returned HTTP headers:
# X-RateLimit-Limit	The maximum number of requests you're permitted to make per hour.
# X-RateLimit-Remaining	The number of requests remaining in the current rate limit window.
# X-RateLimit-Reset	The time at which the current rate limit window resets in UTC epoch seconds.

# Convert epoch to a human-readable form:
# http://www.convert-unix-time.com/
# date -d @1619250770
date -d @$(curl -s https://api.github.com/rate_limit | jq -r ".resources.core.reset")
```
------
* Github webhooks (for read-only copy update automation)
    * https://docs.github.com/en/developers/webhooks-and-events/webhooks
    * https://blog.bearer.sh/consume-webhooks-with-python/
    * Sinatra appears to be more simple to setup: http://sinatrarb.com/
        * See "Configuring your server to receive payloads" section in Github docs
        * https://stackoverflow.com/questions/30027248/running-ruby-sinatra-inside-a-docker-container-not-able-to-connect-via-mac-host
------

* https://stackoverflow.com/questions/1967370/git-replacing-lf-with-crlf/20653073#20653073
```batch
subl "%ProgramFiles%\git\etc\gitconfig"
```
``` shell
# View added, but not committed changes
git diff --cached [myfile.txt]

# work with a different path instead of current working directory
git --git-dir /path/to/repo/.git --work-tree /path/to/repo status
```

### Cheat Sheet
```shell
# Create a new repo
git clone https://urs
cd repo-name
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

# Clone a repository and download submodules simultaneously
git clone --recursive https://url

# View config
git config [--global] –list

# Add all files recursively
git add .

# Undo add
git reset

# Undo commit that hasn't been pushed
git reset HEAD~
# Reverting changes to tracked files:
git reset --hard HEAD~
# [!] Previous command is dangerous. Review what will be reset
git log -3 --stat
git reset --hard previous_commit_hash

# Undo merge commit after "git pull" if remote has new commits
# http://kernowsoul.com/blog/2012/06/20/4-ways-to-avoid-merge-commits-in-git/
git log -3 --stat
git reset --hard previous_commit_hash
git pull --rebase

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
# For a single file
git checkout HEAD -- file.txt

# Modify unpushed commit message (edit existing text in editor)
git commit --amend
# Set directly
git commit --amend -m "New commit message"

# Diff with previous commit
git diff HEAD^ HEAD
# On Windows use ~ unstead of ^
git diff HEAD~ HEAD
# Show a word diff
git diff --color-words 
```

### Initial setup
```bash
source <(curl https://raw.githubusercontent.com/cheretbe/notes/master/files/git/git_intial_setup.sh)
# or
source <(wget -qO- https://raw.githubusercontent.com/cheretbe/notes/master/files/git/git_intial_setup.sh)
```

```bash
# View current config
git config --list [--global]

git config --global color.ui auto

# Avoid trying to guess "user.email" and "user.name", and instead retrieve the values only from the configuration
git config --global user.useConfigOnly true
git config [--global] user.name "user name"
git config [--global] user.email "email"

# Don't quote cyrillic symbols
git config --global core.quotepath false

# Credentials (not needed in recent versions?)
git config --global credential.helper wincred

# Linux
# Cache.  Quite secure because keeps data only in memory. It’s fine for security, but every
# time you open new session, you need to type credentials again. Memory is purged after 900 seconds
# (15 min) by default, but it can be changed with optional timeout parameter
# 1 hour (3600 seconds)
git config --global credential.helper 'cache --timeout=3600'
# [!!!] warning: stores in plaintext!
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
* https://medium.com/@porteneuve/mastering-git-submodules-34c65e940407

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
# Update all branches
git pull --all
# Make sure you are on master branch
git branch
# If not switch to it
git checkout master
# Merge (--no-ff skips "fast-forward")
git merge develop --no-ff
# View current tag
git describe --abbrev=0 --tags
# Add a tag
git tag -a 1.1 -m "version 1.1"
git push --follow-tags
# Switch back to develop
git checkout develop

# View graph (a dog: -*a*ll --*d*ecorate --*o*neline --*g*raph)
git log --all --decorate --oneline --graph

# Push a new local branch to a remote Git repository and track it
# 1. Create
git checkout -b feature_branch_name
# 2. Edit, add and commit files
# 3. Push the branch to the remote repository:
git push -u origin feature_branch_name

# Get commit a tag points to (git rev-parse tag_name returns the SHA1 of the tag object itself)
git rev-list -n 1 tag_name
# Short hash
git rev-list -n 1 --abbrev-commit tag_name
```
### Github backup
http://github-backup.branchable.com/
```
# Check if gcc is actually needed
sudo apt install haskell-stack gcc zlib1g-dev libstdc++-5-dev g++
stack upgrade
/home/<user>/.local/bin/stack install --install-ghc
```
### .gitattributes Files

Powerhsell (Windows)
```
# Set default behaviour, in case users don't have core.autocrlf set.
* text=auto

# Explicitly declare text files we want to always be normalized and converted
# to native line endings on checkout.
*.md            text
*.gitattributes text

# Declare files that will always have CRLF line endings on checkout.
*.ps1    text  eol=crlf
*.psm1   text  eol=crlf
*.psd1   text  eol=crlf
*.psc1   text  eol=crlf
*.ps1xml text  eol=crlf
*.clixml text  eol=crlf
*.xml    text  eol=crlf
*.txt    text  eol=crlf
*.bat    text  eol=crlf

# Denote all files that are truly binary and should not be mergeable.
*.dll binary
*.exe binary
```

```shell
# Determine if Git handles a file as binary or as text
git merge-file /dev/null /dev/null file-to-test
# Error message absence indicates NOT a binary file
```
* https://stackoverflow.com/questions/6119956/how-to-determine-if-git-handles-a-file-as-binary-or-as-text
* https://salferrarello.com/git-file-force-binary/
