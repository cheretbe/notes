* https://core.telegram.org/bots#6-botfather
    * Create a bot and get its token (? - start it with username if getting message that the name is not unique. E.g. `username_blah_bot`)
    * Get chat id: `curl https://api.telegram.org/bot$MY_TG_BOT_TOKEN/getUpdates | jq`
        * If the list is empty for newly created bot, just click start in the chat with it

* Sending a message using curl: https://gist.github.com/dideler/85de4d64f66c1966788c1b2304b9caf1
    * see also notes below
* Full-fledged command-line tool to send messages (could be used **directly from a Python script**): https://github.com/rahiel/telegram-send

```python
#!/usr/bin/env python3

import requests

def check_http_reply(reply):
    if reply.status_code != 200:
        raise Exception("HTTP call has failed. Status code: {code} - {text}".format(code=reply.status_code, text=reply.text))

def send_message_to_telegram_chat(chat_id, tg_bot_token, message, silent=False):
    reply = requests.post(
        url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage",
        data = {
           "chat_id": chat_id,
           "parse_mode": "HTML",
           "text": message,
           "disable_web_page_preview": "true",
           "disable_notification": str(silent)
        }
    )
    check_http_reply(reply)

def send_document_to_telegram_chat(chat_id, tg_bot_token, document):
    requests.post(
        url = f"https://api.telegram.org/bot{tg_bot_token}/sendDocument",
        data = { "chat_id": chat_id },
        files = { "document": document }
    )

send_message_to_telegram_chat(
    chat_id="000000000",
    tg_bot_token="000000000:AAAA00aaaa00000000000000000000000_A",
    message="test message"
)
```

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
