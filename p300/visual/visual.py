import pathlib
from datetime import datetime

from p300.config import EXPORT_RECORDED_DATA
from p300.emotiv.lsl_client import Emotiv
from p300.utils import data_to_raw
from p300.visual.stimulus import Stimulus
from p300.visual.ui import UI
import time


class Visual:
    NUM_STIMULUS = 10

    def __init__(self, *args):
        self.emotiv = Emotiv()
        self.ui = UI(callback=self.callback)

    def start(self):
        self.ui.start()

    def callback(self):
        time.sleep(3)
        self.emotiv.start()

        stimulus = []
        for _ in range(self.NUM_STIMULUS):
            stimulus.append(Stimulus(1))
            self.ui.highlight()

        data = self.emotiv.stop()

        raw = data_to_raw(data, stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/visual_{}_raw.fif".format(path.parent.parent, datetime.now()))
