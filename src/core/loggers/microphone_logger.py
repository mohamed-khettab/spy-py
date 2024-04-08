from sounddevice import rec, wait
from scipy.io.wavfile import write
from os.path import join
from time import sleep


from config.config_loader import get_section_config
from core.utils.logging_utils import m
class MicrophoneLogger:
    def __init__(self) -> None:
        pass