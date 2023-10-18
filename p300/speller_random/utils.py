import glob
import random
from collections import defaultdict
from typing import List

import mne
import numpy as np
from mne import Info, create_info, Epochs
from mne.io.array import RawArray

from p300.config import GRID_SIZE, EPOCHS_TMIN, EPOCHS_TMAX, LOAD_PREBUILD_EPOCHS, SRATE
from p300.speller.stimulus import Stimulus, StimulusHelper



def encede_targets(arr: list):
    d = 0
    for el in arr:
        d += 2 ** el
    return float(d)


# encode to arr from encede_targets
def decode_target(d: int):
    arr = []
    i = 0
    while d > 0:
        if d % 2 == 1:
            arr.append(i)
        d //= 2
        i += 1
    return arr



def data_to_raw(raw_data, stimulus: List[Stimulus]) -> RawArray:
    data = [d + [0] + [0] for d in raw_data]
    i = 0
    while len(stimulus):
        s = stimulus.pop(0)

        while i < len(raw_data) and raw_data[i][14] < s.time:
            i += 1

        if i < len(raw_data):
            data[i][15] = s.stim_id
            data[i][16] = encede_targets(s.targets)

    info = get_info()
    data = np.array(data).T
    return RawArray(data, info)


def get_info() -> Info:
    ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7',
                'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

    info = create_info(
        sfreq=SRATE,
        ch_names=ch_names + ['time'] + ['STIM'] + ['targets'],
        ch_types=['eeg'] * len(ch_names) + ['misc'] + ['stim'] + ['misc'] 
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


def rand(target, n, k):
    # take k random numbers from 0 to GRID_SIZE - 1
    # not take the same number twice
    # not take adjacent numbers by raw and column
    # target should not be repeated twice in a row


    def get_rand():
        out = []
        possible_numbers = list(range(GRID_SIZE * GRID_SIZE))

        while len(out) < k:
            num = random.choice(possible_numbers)

            possible_numbers.remove(num)
            # remove adjacent numbers if possible

            if num - 1 in possible_numbers:
                possible_numbers.remove(num - 1)
            
            if num + 1 in possible_numbers:
                possible_numbers.remove(num + 1)
            
            if num - GRID_SIZE in possible_numbers:
                possible_numbers.remove(num - GRID_SIZE)
            
            if num + GRID_SIZE in possible_numbers:
                possible_numbers.remove(num + GRID_SIZE)

            out.append(num)
        
        return out
    

    out = []
    i = 0
    last_target_index = -10000
    while len(out) < n:
        rand_list = get_rand()
        # if target in rand_list and i - last_target_index < 1:
        #     i += 1
        #     continue
        # if target in rand_list:
        #     last_target_index = i
        
        out.append(rand_list)
        i += 1
    return out 


        
   
