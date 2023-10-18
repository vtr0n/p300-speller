import pathlib
from collections import defaultdict
from datetime import datetime
from random import randint

import mne
from mne.preprocessing import ICA

from p300.config import GRID_SIZE, EXPORT_RECORDED_DATA, EPOCHS_TMIN, EPOCHS_TMAX, TRAIN_EPOCH_NUM, PREDICT_EPOCH_NUM
from p300.emotiv.lsl_client import Emotiv
from p300.speller_random.model import get_model
from p300.speller_random.stimulus import Stimulus, StimulusHelper
from p300.speller_random.ui import UI
from p300.speller_random.utils import data_to_raw, rand, load_prebuild_epochs


class SpellerRandom:
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

        rand_list = rand(target, TRAIN_EPOCH_NUM, 4)
        stimulus = []

        for highligth in rand_list:
            if self.state == self.STATE_STOP:
                return   
            
            stim = Stimulus(StimulusHelper.getTarget(target in highligth), highligth)
            stimulus.append(stim)
            self.ui.highlight(highligth)

        data = self.emotiv.stop()

        raw = data_to_raw(data, stimulus.copy())
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/train_{}_target_{}_raw.fif".format(path.parent.parent, datetime.now(), target), fmt='double')

        ica = ICA(n_components=14, max_iter="auto", random_state=97)

        ica.fit(raw)
        ica.apply(raw)
        raw.filter(1, 30)
        
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

        rand_list = rand(-100, PREDICT_EPOCH_NUM, 4)
        stimulus = []

        for highligth in rand_list:
            if self.state == self.STATE_STOP:
                return
            
            stim = Stimulus(StimulusHelper.NON_TARGET, highligth)
            stimulus.append(stim)
            self.ui.highlight(highligth)
        
        data = self.emotiv.stop()
        raw = data_to_raw(data, stimulus.copy())
        if EXPORT_RECORDED_DATA:
            path = pathlib.Path(__file__).parent.resolve()
            raw.save("{}/data/predict_{}_raw.fif".format(path.parent.parent, datetime.now()), fmt='double')

        raw.filter(1, 30, method='iir')
        events = mne.find_events(raw)
        event_id = {'Target': 2 ,'b': 1}
        ep = mne.Epochs(raw, events, event_id, tmin=EPOCHS_TMIN, tmax=EPOCHS_TMAX, baseline=None, preload=True,
                        on_missing='ignore')
        ep.pick_types(eeg=True)

        x = ep.get_data()
        p_col, p_row = self._find_cell(x, stimulus)
        self.ui.highlight_prediction(p_row, p_col)

    def stop(self):
        self.emotiv.stop()
        self.state = self.STATE_STOP

    def _find_cell(self, x, stimulus):
        predictions = self.model.predict(x)
        predictions_proba = self.model.predict_proba(x)

        score = defaultdict(int)
        score_proba = defaultdict(int)
        count = defaultdict(int)
        goals_num = 0
        for st, pred, pred_proba in zip(stimulus, predictions, predictions_proba):    
            if pred == StimulusHelper.TARGET:  
                goals_num += 1
            for num in st.targets:
                score[num] += 1 if pred == StimulusHelper.TARGET else 0
                score_proba[num] += pred_proba[0]
                count[num] += 1
        
        # normalize
        for key in score:
            score_proba[key] /= count[key]
        
        # find key for max value
        result = max(score_proba, key=score_proba.get)

        import string
        arr = list(string.ascii_uppercase) + ['_'] + list(range(1, 10))
        # kv = (a -> 0, b = 1, )

        kv = {}
        k = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                kv[j*GRID_SIZE + i] = arr[k]
                k += 1

        ans = []
        for i in range(len(score)):
            ans.append([kv[i], score[i], round(score_proba[i], 3)])
            #print(kv[i], score[i], round(score_proba[i], 3))

        #print('goals_num', goals_num)
        ans.sort(key=lambda x: x[2], reverse=True)
        print(ans)

        p_col = result // GRID_SIZE
        p_row = result % GRID_SIZE

        return p_col, p_row
