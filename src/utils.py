import os
import ctypes
import platform
import sys
import requests
import tkinter.messagebox
def get_platform():
    return platform.system()

def is_admin():
    if get_platform() == "Windows":
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        try:
            return os.getuid() == 0
        except AttributeError:
            return False

def send_webhook(url, message=None, file=None):
    data = {
        "username": "SpyPy"
    }
    if message:
        data["content"] = message
    if file:
        data["file"] = file
    requests.post(url, json=data)

def is_exe():
    return getattr(sys, "frozen", False)

def display_error_message(title, message):
    if get_platform() == "Windows":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
    else:
        tkinter.messagebox.showerror(title=title, message=message) 
        #TODO find a better looking error msg
