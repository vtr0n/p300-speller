import pathlib
from datetime import datetime

from p300.music.stimulus import Stimulus, StimulusHelper
from p300.music.ui import UI
from p300.config import EXPORT_RECORDED_DATA
from p300.emotiv.emotiv import Emotiv
import musicalbeeps
import time
import random

from p300.utils import data_to_raw


class Music:
    def __init__(self, client_id, client_secret, license):
        self.model = None

        self.emotiv = Emotiv(client_id, client_secret, license)
        self.emotiv.open()
        self.ui = UI(callbacks=[self.play])
        self.player = musicalbeeps.Player(volume=0.3, mute_output=False)

    def start(self):
        self.ui.start()

    def play(self):
        self.emotiv.start()
        stimulus = []
        for i in range(0, 60):

            if random.randint(0, 1) == 0:
                stimulus.append(Stimulus(StimulusHelper.C5))
                self.player.play_note('C5', 0.5)
            else:
                stimulus.append(Stimulus(StimulusHelper.C6))
                self.player.play_note('C6', 0.5)

            time.sleep(1)

        self.emotiv.stop()
        raw = data_to_raw(self.emotiv.get_data(), stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/music_{}_raw.fif".format(path.parent, datetime.now()))
