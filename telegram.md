* https://core.telegram.org/bots#6-botfather
* Sending a message using curl: https://gist.github.com/dideler/85de4d64f66c1966788c1b2304b9caf1
    * see also notes below
* Full-fledged command-line tool to send messages (could be used **directly from a Python script**): https://github.com/rahiel/telegram-send

```shell
# Get chat ID using proxy
curl -x 192.168.1.1:1111 https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates| jq .result[0].message.chat.id

# Send a message using proxy
curl -X POST \
    -x 192.168.1.1:1111 \
    -H 'Content-Type: application/json' \
    -d '{"chat_id": "111111111", "text": "This is a test from curl", "disable_notification": false}' \
    https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage
```
