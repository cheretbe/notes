#!/usr/bin/env python3

import os
import argparse
import subprocess
import pathlib
import random
import requests


def check_http_reply(reply):
    if reply.status_code != 200:
        raise Exception("HTTP call has failed. Status code: {code} - {text}".format(code=reply.status_code, text=reply.text))
    
def send_message_to_telegram_chat(chat_id, tg_bot_token, message, silent=False):
    reply = requests.post(
        url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage",
        data = {
            "chat_id": chat_id,
            # "parse_mode": "HTML",
            "parse_mode": "Markdown",
            "text": message,
            "disable_web_page_preview": "true",
            "disable_notification": str(silent)
        }
    )
    check_http_reply(reply)

def main(args):
    if args.sound:
        sounds = ["jobs_done.mp3", "work_completed.mp3", "work_complete.mp3"]
        proc = subprocess.Popen(
            ["ffplay", "-v", "0", "-nodisp", "-autoexit", (pathlib.Path(__file__).resolve().parents[0] / "mp3" / random.choice(sounds))],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # ffplay returns 0 even the file is missing, no point waiting for it
        # 0.5 seconds
        # proc.communicate(timeout=.5)
        # print(proc)

    send_message_to_telegram_chat(
        chat_id=args.chat_id,
        tg_bot_token=args.tg_bot_token,
        message="Job is done on *" + subprocess.check_output(["hostname", "-f"], universal_newlines=True) + f"* in {os.getcwd()}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("chat_id")
    parser.add_argument("tg_bot_token")
    parser.add_argument("-s", "--sound", action="store_true", default=False, help="Play sound locally")

    args = parser.parse_args()
    main(args)