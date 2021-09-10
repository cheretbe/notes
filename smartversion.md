### GUI

:warning: Set temp directory if needed: `Options` > `Application Settings` > `Select a custom temporary directory`

### Command line

```shell
# Assuming that smv (http://www.smartversion.com) is installed in ~/bin

# Build a patch
# Test settings: https://forums.mydigitallife.net/threads/smartversion-tools-scripts.79415/page-14#post-1599203
date; time smv BuildPatch [SvfFile] [OldFile] [NewFile] -nbhashbits 24 -compressratio 49 -sha1 -sha25; finished

# List files
smv l file.svf
smv lv file.svf [-v 0]

# Extract
smv x file.svf -v 0
smv x file.svf -v 1
# When in a subdir of *.svf and *.iso
find .. -iname '*.svf' -exec echo {} \; -exec smv x {} -br .. \; ;finished
```
