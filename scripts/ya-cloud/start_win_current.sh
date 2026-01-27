#!/bin/bash

set -euo pipefail

current_state=$(yc compute instance get --name "windows-current" --profile default --format json | jq -r '.status')

if [ "${current_state}" = "RUNNING" ]; then
  echo '"windows-current" VM is already running'
  # ip_address="51.250.99.13"
else
  echo 'Starting "windows-current" VM'
  vm_data=$(yc compute instance start --name "windows-current" --profile default --format json)
  ip_address=$(echo "$vm_data" | jq -r '.network_interfaces[0].primary_v4_address.one_to_one_nat.address')

  echo "IP address: $ip_address"
  echo "Getting DNS zone ID"
  dns_zone_id=$(curl -s -f -X GET -H "Authorization: Bearer $TF_VAR_cf_api_token" https://api.cloudflare.com/client/v4/zones/?name=chere.one | jq -r ".result[].id")
  echo "Getting DNS record ID"
  dns_record_id=$(curl -s -f -X GET -H "Authorization: Bearer $TF_VAR_cf_api_token" "https://api.cloudflare.com/client/v4/zones/$dns_zone_id/dns_records?type=A&name=$AO_CURRENT_VM_FQDN" | jq -r '.result[].id')
  echo "Setting DNS record for windows-current.chere.one to $ip_address"
  curl -s -f -X PATCH "https://api.cloudflare.com/client/v4/zones/$dns_zone_id/dns_records/$dns_record_id" \
    -H "Authorization: Bearer $TF_VAR_cf_api_token" \
    -H "Content-Type: application/json" \
    --data '{"type": "A", "name": "'$AO_CURRENT_VM_FQDN'", "content": "'$ip_address'", "id": "'$dns_record_id'", "zone_id": "'$dns_zone_id'", "ttl": 60, "proxied": false}' \
    > /dev/null

  echo "Waiting for RDP to become available"
  # --foreground is for Ctrl+C to work
  timeout --foreground 5m bash -c "until nc -z $AO_CURRENT_VM_FQDN $AO_CURRENT_VM_PORT; do sleep 1; done"
  if [ $? -ne 0 ]; then
    >&2 echo "Timeout waiting for $AO_CURRENT_VM_FQDN:$AO_CURRENT_VM_PORT to become available"
    exit 1
  fi
  echo "OK"
fi
