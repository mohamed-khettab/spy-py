from sounddevice import rec, wait
from scipy.io.wavfile import write
from os.path import join
from time import sleep
import sys

class MicrophoneLogger:
    def __init__(self) -> None:
        pass