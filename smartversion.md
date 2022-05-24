### GUI

:warning: Set temp directory if needed: `Options` > `Application Settings` > `Select a custom temporary directory`

### Command line

```shell
# Assuming that smv (http://www.smartversion.com) is installed in ~/bin

# Build a patch
# https://forums.mydigitallife.net/threads/smartversion-tools-scripts.79415/page-14#post-1599203
date; time smv BuildPatch [SvfFile] [OldFile] [NewFile] -nbhashbits 24 -compressratio 192 -sha1 -sha25; finished

# List files
smv l file.svf
smv lv file.svf [-v 0]

# Extract
smv x file.svf -v 0
smv x file.svf -v 1
find . -iname '*.svf' -exec echo {} \; -exec smv x {} -br . \; ;finished
```

```python
import pathlib
import subprocess

def is_x64(iso_path):
    return "_x64_dvd_" in iso_path.lower()

base_isos = {
    True:  None,
    False: None,
}

for child_obj in pathlib.Path.cwd().iterdir():
    if child_obj.is_file() and (child_obj.suffix.lower() == ".iso"):
        if child_obj.name.lower().startswith("en-us"):
            base_isos[is_x64(child_obj.name)] = child_obj.name

for child_obj in pathlib.Path.cwd().iterdir():
    if child_obj.is_file() and (child_obj.suffix.lower() == ".iso"):
        if not child_obj.name.lower().startswith("en-us"):
            smv_cmd = [
                "smv", "BuildPatch", child_obj.with_suffix(".svf").name,
                base_isos[is_x64(child_obj.name)], child_obj.name,
                "-nbhashbits", "24", "-compressratio", "192", "-sha1", "-sha25"
            ]
            print(f"\n{smv_cmd}")
            subprocess.check_call(smv_cmd)

```
