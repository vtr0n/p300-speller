from typing import List

import mne
from mne import Epochs
from mne.decoding import Vectorizer
from pyriemann.estimation import Xdawn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline, Pipeline


def get_model(epoch_list: List[Epochs]) -> Pipeline:
    epochs = mne.concatenate_epochs(epoch_list)

    X = epochs.get_data()
    y = epochs.events[:, -1]

    model = make_pipeline(Xdawn(2, classes=[1]), Vectorizer(), LDA(shrinkage='auto', solver='eigen'))
    # model = make_pipeline(Vectorizer(), StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(X, y)

    return model
