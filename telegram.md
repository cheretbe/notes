* https://core.telegram.org/bots#6-botfather
* Sending a message using curl: https://gist.github.com/dideler/85de4d64f66c1966788c1b2304b9caf1
    * see also notes below
* Full-fledged command-line tool to send messages (could be used **directly from a Python script**): https://github.com/rahiel/telegram-send

```shell
# Get chat ID using proxy
# [!] If the result is empty, just send something to the bot using GUI client
curl -x 192.168.1.1:1111 -s https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates | jq .result[].message.chat.id

# Send a message using proxy
# Remove "disable_notification" setting to enable notification
curl -X POST \
    -x 192.168.1.1:1111 \
    -H 'Content-Type: application/json' \
    -d '{"chat_id": "111111111", "text": "'$(hostname -f)': test from curl", "disable_notification": false}' \
    https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage
```

* https://towardsdatascience.com/proper-ways-to-pass-environment-variables-in-json-for-curl-post-f797d2698bf3
```bash
generate_message_data()
{
  c_time="$(date +'%_H:%M')"
  cat <<EOF
{
  "chat_id": "000000000",
  "text": "${c_time} - $(hostname -f)",
  "disable_notification": false 
}
EOF
}

curl -s -X POST \
    -H 'Content-Type: application/json' \
    -d "$(generate_message_data)" \
    https://api.telegram.org/bot000000000:AAAA00aaaa00000000000000000000000_A/sendMessage 1>/dev/null
```
