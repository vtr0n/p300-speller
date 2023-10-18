from typing import List

import mne
import math
from mne import Epochs
from mne.decoding import Vectorizer
from pyriemann.estimation import Xdawn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.pipeline import make_pipeline, Pipeline


def get_model(epoch_list: List[Epochs]) -> Pipeline:
    epochs = mne.concatenate_epochs(epoch_list)

    X = epochs.get_data()
    y = epochs.events[:, -1]

    model = make_pipeline(Xdawn(2, classes=[1]), Vectorizer(), LDA(shrinkage='auto', solver='eigen'))
    # model = make_pipeline(Vectorizer(), StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(X, y)


    cv = StratifiedShuffleSplit(n_splits=20, test_size=0.4, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring='roc_auc')
    
    # mean
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    return model
