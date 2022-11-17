
### Unsorted
#### Merging branches
* :warning: Review when (once again) having trouble with merge:
* https://www.atlassian.com/git/tutorials/using-branches/git-merge
* https://stackoverflow.com/questions/8716130/git-branches-diverged-how-to-proceed/8716401#8716401

Branches diverged
```shell
git rebase main
git status
# On branch add_feature
# Your branch and 'origin/add_feature' have diverged,
# and have 5 and 3 different commits each, respectively.
#   (use "git pull" to merge the remote branch into yours)
git pull --rebase
```


```shell
# [!!!] backup before proceeding

# Option 1
git format-patch -M @{upstream}
git reset --hard @{upstream}

git am 0001-blah-blah.patch
git am 0002-blah-blah.patch
# ...

# Option 2
# Create a spare branch with your work on it
git branch scrap
# Then reset your branch to the upstream
git reset --hard @{upstream}

# Then cherry-pick the commits over
git cherry-pick scrap~6
git cherry-pick scrap~5
git cherry-pick scrap~4
# ...

# Then trash the scrap branch
git branch -D scrap
```

---------------------------------------------
* https://docs.gitlab.com/ee/user/project/repository/branches/default.html#instance-level-custom-initial-branch-name

```shell
git config --global merge.tool meld
git merge master
git mergetool

# Merge dry-run
# https://stackoverflow.com/questions/501407/is-there-a-git-merge-dry-run-option/501461#501461
git merge --no-commit --no-ff $BRANCH
# Examine staged changes
git diff --cached
# Undo the merge
git merge --abort
```

### .gitignore examples

Store directory in the repo, ignoring it's contents
```
*
*/
!.gitignore
```

### .gitattributes examples

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


### Github

* https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
* To compare different versions of your repository, append /compare to your repository's path

```shell
# Get latest release
release_data=$(curl -s https://api.github.com/repos/backuppc/backuppc-xs/releases/latest)
backuppc_xs_ver=$(echo ${release_data} | jq -r ".tag_name")
backuppc_xs_tar=$(echo ${release_data} | jq -r ".assets[0].name")
wget $(echo ${release_data} | jq -r ".assets[0].browser_download_url")
tar -xzvf ${backuppc_xs_tar}
cd BackupPC-XS-${backuppc_xs_ver}

# View current requests rate limits, both authenticated and non-authenticated (per IP)
curl -s -H "Authorization: token ${AO_GITHUB_OAUTH_TOKEN}" https://api.github.com/rate_limit | jq -r ".resources.core"; \
  curl -s https://api.github.com/rate_limit | jq -r ".resources.core"

# Alternative authentication
curl -i -u cheretbe:${AO_GITHUB_OAUTH_TOKEN} https://api.github.com/users/cheretbe

curl -s https://api.github.com/rate_limit
curl -s -u cheretbe:${AO_GITHUB_OAUTH_TOKEN}
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

### Scripting
```shell
# List local branches
git for-each-ref refs/heads --format='%(refname:short)'
# Get current branch
git rev-parse --abbrev-ref HEAD

# Check if a repo needs pulling
git fetch --quiet
# compare output of the following two commands
# -n <number>, --max-count=<number> Limit the number of commits to output
# @{u} means HEAD@{upstream}, @ means HEAD
git rev-list -n 1 @{u}
git rev-list -n 1 @
# Tests
git rev-list -n 1 HEAD@{upstream}; git rev-list -n 1 HEAD
# revert last pull https://stackoverflow.com/questions/5815448/how-to-undo-a-git-pull/5815626#5815626
git reset --keep HEAD@{1}
# for newly cloned repo HEAD@{1} is undedfined, just go 2 commits back
git reset --keep HEAD~2
```

### References
* https://stackoverflow.com/questions/17910096/what-does-the-at-sign-symbol-character-mean-in-git
* https://stackoverflow.com/questions/964876/head-and-orig-head-in-git
* https://stackoverflow.com/questions/2304087/what-is-git-head-exactly

The at-sign `@`, without a leading branch/reference name and ordinal `{n}` suffix like `HEAD@{1}` and `master@{1}`
is just a synonym/alias/shortcut for the special Git reference `HEAD`.

### Cheat Sheet
```shell
# view history of changes for single file (#revisions)
git log -- filename
# use --follow to include history of renames
git log --follow -- filename
# view actual changes
git log -p -- filename

# Revert a single file to a previous commit
git checkout <commit> filename


# View added, but not committed changes
git diff --cached [myfile.txt]
# In more recent versions of git, --staged is a synonym for --cached
git diff --staged

# work with a different path instead of current working directory
git --git-dir /path/to/repo/.git --work-tree /path/to/repo status



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

Per-server setup<br>
`.giconfig`:
```
# git 2.36+
# add-apt-repository ppa:git-core/ppa
[includeIf "hasconfig:remote.*.url:https://github.com/**"]
        # It's ok to use ~ here
        path = .github-git-config
```
`.github-git-config`:
```
[user]
        name = user
        email = user@ptsecurity.com
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

# As of August 13 2021 Github is no longer accepting account passwords when authenticating Git operations.
# Create personal access token (Settings => Developer Settings => Personal Access Token => Generate New Token),
# then just use it in a credential manager instead of the password

# Credentials (not needed in recent versions?)
git config --global credential.helper wincred

# Linux
# libsecret, view with Gnome keyring (seahorse)
# https://stackoverflow.com/questions/36585496/error-when-using-git-credential-helper-with-gnome-keyring-as-sudo/40312117#40312117
# [!] May need reboot on Ubuntu 20.04 to work properly
sudo apt-get install build-essential libsecret-1-0 libsecret-1-dev
cd /usr/share/doc/git/contrib/credential/libsecret
sudo make
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret

# Cache.  Quite secure because keeps data only in memory. It’s fine for security, but every
# time you open new session, you need to type credentials again. Memory is purged after 900 seconds
# (15 min) by default, but it can be changed with optional timeout parameter
# 1 hour (3600 seconds)
git config --global credential.helper 'cache --timeout=3600'
# [!!!] warning: stores in plaintext! (~/.git-credentials)
git config --global credential.helper store

git config --global push.default simple
```

### LFS

```shell
# A fix for files, that should have been added as LFS pointers according to .gitattributes,
# but weren't (Encountered N file(s) that should have been pointers, but weren't)
git add . --renormalize
git commit -m "Fix LFS pointers to some binary files"
```

### Troubleshooting
``` shell
# Increase verbosity
git 'command' --verbose
# or
git 'command' -v
# Also useful
git 'command' --dry-run
# https://github.com/git/git/blob/master/Documentation/git.txt
# GIT_TRACE_SETUP
GIT_CURL_VERBOSE=1 git 'command'
GIT_TRACE_PACKET=2 GIT_TRACE_CURL_NO_DATA=1 git 'command'
# On Windows
SET GIT_CURL_VERBOSE=1
SET GIT_TRACE_PACKET=2
SET GIT_TRACE_CURL_NO_DATA=1
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
