#!/bin/bash

service nginx configtest
if [ $? -eq 0 ]; then
  echo "Reloading nginx configuration"
  service nginx force-reload
else
  tail -10 /var/log/nginx/error.log
fi
