import pathlib
from collections import defaultdict
from datetime import datetime
from random import randint

import mne

from p300.config import GRID_SIZE, EXPORT_RECORDED_DATA, EPOCHS_TMIN, EPOCHS_TMAX, TRAIN_EPOCH_NUM, PREDICT_EPOCH_NUM
from p300.emotiv.emotiv import Emotiv
from p300.model import get_model
from p300.stimulus import Stimulus, StimulusHelper
from p300.ui import UI
from p300.utils import data_to_raw, rand, load_prebuild_epochs


class Speller:
    STATE_ACTIVE = 1
    STATE_STOP = 2

    def __init__(self, client_id, client_secret, license):
        self.epochs = load_prebuild_epochs()
        self.model = None
        if len(self.epochs):
            self.model = get_model(self.epochs)

        self.emotiv = Emotiv(client_id, client_secret, license)
        self.emotiv.open()
        self.ui = UI(callbacks=[self.train, self.predict, self.stop])
        self.state = self.STATE_ACTIVE

    def start(self):
        self.ui.start()

    def train(self):
        target = randint(0, GRID_SIZE * GRID_SIZE)
        target_col = target // GRID_SIZE
        target_row = target % GRID_SIZE

        self.emotiv.start()
        self.ui.highlight_target(target_row, target_col)

        self.state = self.STATE_ACTIVE

        rand_list = rand(TRAIN_EPOCH_NUM)
        stimulus = []

        for is_col, num in rand_list:
            if self.state == self.STATE_STOP:
                return
            if is_col:
                is_target = num == target_col
                stimulus.append(Stimulus(StimulusHelper.TARGET) if is_target else Stimulus(StimulusHelper.NON_TARGET))
                self.ui.highlight_col(num)
            else:
                is_target = num == target_row
                stimulus.append(Stimulus(StimulusHelper.TARGET) if is_target else Stimulus(StimulusHelper.NON_TARGET))
                self.ui.highlight_row(num)

        self.emotiv.stop()

        raw = data_to_raw(self.emotiv.get_data(), stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/train_{}_raw.fif".format(path.parent, datetime.now()))

        raw.filter(1, 30, method='iir')
        events = mne.find_events(raw)
        event_id = StimulusHelper.get_train_event_id()
        ep = mne.Epochs(raw, events, event_id, tmin=EPOCHS_TMIN, tmax=EPOCHS_TMAX, baseline=None, preload=True)

        ep.pick_types(eeg=True)
        self.epochs.append(ep)

        self.model = get_model(self.epochs)

    def predict(self):
        self.emotiv.start()
        self.state = self.STATE_ACTIVE
        self.ui.countdown()

        rand_list = rand(PREDICT_EPOCH_NUM)
        stimulus = []

        for is_col, num in rand_list:
            if self.state == self.STATE_STOP:
                return
            if is_col:
                stimulus.append(Stimulus(StimulusHelper.from_col(num)))
                self.ui.highlight_col(num)
            else:
                stimulus.append(Stimulus(StimulusHelper.from_row(num)))
                self.ui.highlight_row(num)

        self.emotiv.stop()

        raw = data_to_raw(self.emotiv.get_data(), stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/predict_{}_raw.fif".format(path.parent, datetime.now()))

        raw.filter(1, 30, method='iir')
        events = mne.find_events(raw)
        event_id = StimulusHelper.get_prediction_event_id()
        ep = mne.Epochs(raw, events, event_id, tmin=EPOCHS_TMIN, tmax=EPOCHS_TMAX, baseline=None, preload=True,
                        on_missing='ignore')
        ep.pick_types(eeg=True)

        x = ep.get_data()
        predictions = self.model.predict(x)

        p_col, p_row = self._find_cell(predictions, ep.events)
        self.ui.highlight_prediction(p_row, p_col)

    def stop(self):
        self.emotiv.stop()
        self.state = self.STATE_STOP

    def _find_cell(self, predictions, events):
        score = defaultdict(int)
        for pred, ev in zip(predictions, events):
            _, _, val = ev
            score[val] += 1 if pred == StimulusHelper.TARGET else -1

        p_col = p_row = 0
        p_col_val = p_row_val = float('-inf')
        for key in score:
            val = score[key]
            if StimulusHelper.is_col(key) and val > p_col_val:
                p_col_val = val
                p_col = StimulusHelper.to_col(key)
            if StimulusHelper.is_row(key) and val > p_row_val:
                p_row_val = val
                p_row = StimulusHelper.to_row(key)

        return p_col, p_row
