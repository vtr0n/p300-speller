import glob
import random
from collections import defaultdict
from typing import List

import mne
import numpy as np
from mne import Info, create_info, Epochs
from mne.io.array import RawArray

from p300.config import GRID_SIZE, EPOCHS_TMIN, EPOCHS_TMAX, LOAD_PREBUILD_EPOCHS
from p300.stimulus import Stimulus, StimulusHelper


def data_to_raw(raw_data, stimulus: List[Stimulus]) -> RawArray:
    data = [d['eeg'][2:16] + [0] for d in raw_data]
    i = 0
    while len(stimulus):
        s = stimulus.pop(0)

        while i < len(raw_data) and raw_data[i]['time'] < s.time:
            i += 1

        if i < len(raw_data):
            data[i][-1] = s.type

    info = get_info()
    return RawArray(np.array(data).T, info)


def get_info() -> Info:
    ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']
    sfreq = 256

    info = create_info(
        sfreq=sfreq,
        ch_names=ch_names + ['STI 1'],
        ch_types=['eeg'] * len(ch_names) + ['stim']
    )

    return info


def load_prebuild_epochs() -> List[Epochs]:
    if not LOAD_PREBUILD_EPOCHS:
        return []

    files = glob.glob('data/train_*.fif')

    epoch_list = []
    for file in files:
        raw = mne.io.read_raw_fif(file, preload=True)
        raw.filter(1, 30, method='iir')

        events = mne.find_events(raw)

        event_id = StimulusHelper.get_train_event_id()
        epoch = mne.Epochs(raw, events, event_id, tmin=EPOCHS_TMIN, tmax=EPOCHS_TMAX, baseline=None, preload=True,
                           on_missing='ignore')
        epoch.pick_types(eeg=True)
        epoch_list.append(epoch)

    return epoch_list


def rand(n):
    out = []
    col = defaultdict(int)
    row = defaultdict(int)

    i = 0
    k = 0
    while len(out) < n:
        i += 1
        num = random.randint(0, GRID_SIZE - 1)
        if k <= 3:
            if i - col[num] < 5:
                continue

            out.append((True, num))
            col[num] = i
        elif k <= 6:
            if i - row[num] < 5:
                continue

            out.append((False, num))
            row[num] = i
        else:
            k = -1

        k += 1
    return out
