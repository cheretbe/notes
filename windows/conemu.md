## Clink
https://mridgers.github.io/clink/  
Extract zip contents into `c:\Program Files\ConEmu\ConEmu\clink\` (no subdirs, all files should be in this directory)

Settings -> Startup -> Environment: 
```
set clink_profile=c:\Users\username\AppData\Roaming\clink
```
The directory will be created automatically

Add custom completion files

https://github.com/vladimir-kotikov/clink-completions

Extract into `c:\Users\username\AppData\Roaming\clink`

To enable cmd.exe-like tab completion (cycle through options), in
`C:\Program Files\ConEmu\ConEmu\clink\clink_inputrc_base` uncomment the following lines:
```
# Uncomment these two lines for vanilla cmd.exe style completion.
"\t": clink-menu-completion-shim
"\e`Z": clink-backward-menu-completion-shim
```
