Run `/usr/lib/citadel-server/setup` after installation to change user from `root` to `citadel` (check ownership on `/etc/citadel/` after that).
Also, if citserver stops listening on port 504, re-run fixes this.

WebCit (web GUI) settings are in `/etc/default/webcit`

Citadel does not support `/etc/aliases`. To redirect messages on the server, aliases need to be assigned directly to the user accounts. In WebCit: 
  1. Click "Administration" 
  2. Click "Add, change, delete user accounts" 
  3. Select the user and click "Edit address book entry" 
  4. In the box labelled "Internet e-mail aliases" enter as many aliases as you want, one per line. 
