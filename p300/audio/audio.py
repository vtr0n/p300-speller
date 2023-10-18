import pathlib
from datetime import datetime

from p300.audio.stimulus import Stimulus, StimulusHelper
from p300.audio.ui import UI
from p300.config import EXPORT_RECORDED_DATA
from p300.emotiv.lsl_client import Emotiv
import musicalbeeps
import time
import random

from p300.audio.utils import data_audio_to_raw


class Audio:

    EPOCH_NUM = 30
    def __init__(self):
        self.model = None

        self.emotiv = Emotiv()
        self.ui = UI(callbacks=[self.play])
        self.player = musicalbeeps.Player(volume=0.3, mute_output=False)

    def start(self):
        self.ui.start()

    def play(self):
        self.emotiv.start()

        notes = ['C3', 'C4', 'C5', 'C6', 'C7']
        target = 'C7'

        self.player.play_note(target, 0.3)
        time.sleep(3)


        stimulus = []
        for _ in range(0, 50):
            choise = random.choice(notes)
            stimulus.append(Stimulus(StimulusHelper.getId(choise)))
            self.player.play_note(choise, 0.3)
            time.sleep(0.4)
        

        data = self.emotiv.stop()
        raw = data_audio_to_raw(data, stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/audio_{}_target{}_raw.fif".format(path.parent.parent, datetime.now(), target))
