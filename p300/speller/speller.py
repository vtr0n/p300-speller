import pathlib
from collections import defaultdict
from datetime import datetime
from random import randint

import mne
from mne.preprocessing import ICA

from p300.config import GRID_SIZE, EXPORT_RECORDED_DATA, EPOCHS_TMIN, EPOCHS_TMAX, TRAIN_EPOCH_NUM, PREDICT_EPOCH_NUM
from p300.emotiv.lsl_client import Emotiv
from p300.speller.model import get_model
from p300.speller.stimulus import Stimulus, StimulusHelper
from p300.speller.ui import UI
from p300.speller.utils import data_to_raw, rand, load_prebuild_epochs


class Speller:
    STATE_ACTIVE = 1
    STATE_STOP = 2

    def __init__(self):
        self.epochs = load_prebuild_epochs()
        self.model = None
        if len(self.epochs):
            self.model = get_model(self.epochs)

        self.emotiv = Emotiv()
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
                stim = Stimulus(StimulusHelper.getTarget(is_target), target=target, value=num, is_col=1)
                stimulus.append(stim)
                self.ui.highlight_col(num)
            else:
                is_target = int(num == target_row)
                stim = Stimulus(StimulusHelper.getTarget(is_target), target=target, value=num, is_col=0)
                stimulus.append(stim)
                self.ui.highlight_row(num)

        data = self.emotiv.stop()
        raw = data_to_raw(data, stimulus)
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/train_{}_raw.fif".format(path.parent.parent, datetime.now()))

        ica = ICA(n_components=14, max_iter="auto", random_state=97)
        ica.fit(raw)
        ica.apply(raw)
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
                stimulus.append(Stimulus(is_target= 99, target= 99, value= num, is_col= 1))
                self.ui.highlight_col(num)
            else:
                stimulus.append(Stimulus(is_target= 99, target= 99, value= num, is_col= 0))
                self.ui.highlight_row(num)

        data = self.emotiv.stop()
        raw = data_to_raw(data, stimulus.copy())
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/predict_{}_raw.fif".format(path.parent.parent, datetime.now()))

        ica = ICA(n_components=14, max_iter="auto", random_state=97)
        ica.fit(raw)
        ica.apply(raw)
        raw.filter(1, 30, method='iir')
        events = mne.find_events(raw)
        event_id = {'Unknown': 99}
        ep = mne.Epochs(raw, events, event_id, tmin=EPOCHS_TMIN, tmax=EPOCHS_TMAX, baseline=None, preload=True,
                        on_missing='ignore')
        ep.pick_types(eeg=True)

        x = ep.get_data()
        predictions = self.model.predict_proba(x)

        p_col, p_row = self._find_cell(predictions, stimulus)
        self.ui.highlight_prediction(p_row, p_col)

    def stop(self):
        self.emotiv.stop()
        self.state = self.STATE_STOP

    def _find_cell(self, predictions, stimulus):
        score_col = defaultdict(int)
        score_col_cnt = defaultdict(int)

        score_row = defaultdict(int)
        score_row_cnt = defaultdict(int)
        for pred, st in zip(predictions, stimulus):
            if st.is_col == 1:
                score_col[st.value] += pred[0]
                score_col_cnt[st.value] += 1
            else:
                score_row[st.value] += pred[0]
                score_row_cnt[st.value] += 1

        # normalize
        for key in score_col:
            score_col[key] /= score_col_cnt[key]
            print("col key", key, round(score_col[key], 3))
        
        for key in score_row:
            score_row[key] /= score_row_cnt[key]
            print("row key", key, round(score_row[key], 3))


        print(score_col, score_row)
        col = max(score_col, key=score_col.get)
        row = max(score_row, key=score_row.get)

        return col, row
