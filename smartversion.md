### GUI

:warning: Set temp directory if needed: `Options` > `Application Settings` > `Select a custom temporary directory`

### Command line

```shell
# Assuming that smv (http://www.smartversion.com) is installed in ~/bin

# Build a patch
date; time smv BuildPatch [SvfFile] [OldFile] [NewFile]

# List files
smv l file.svf
smv lv file.svf [-v 0]

# Extract
smv x file.svf -v 0
smv x file.svf -v 1
```
