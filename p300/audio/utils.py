from typing import List

import numpy as np
from mne import Info, create_info
from mne.io.array import RawArray

from p300.config import SRATE
from p300.audio.stimulus import Stimulus


def data_audio_to_raw(raw_data, stimulus: List[Stimulus]) -> RawArray:
    data = [d + [0] for d in raw_data]
    i = 0
    while len(stimulus):
        s = stimulus.pop(0)

        while i < len(raw_data) and raw_data[i][14] < s.time:
            i += 1

        if i < len(raw_data):
            data[i][15] = s.type

    info = get_info()
    return RawArray(np.array(data).T, info)


def get_info() -> Info:
    ch_names = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7',
                'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

    info = create_info(
        sfreq=SRATE,
        ch_names=ch_names + ['time'] + ['STIM'],
        ch_types=['eeg'] * len(ch_names) + ['misc'] + ['stim']
    )

    return info
