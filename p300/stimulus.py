import time
from dataclasses import dataclass, field

from p300.config import GRID_SIZE


class StimulusHelper:
    TARGET = 1
    NON_TARGET = 2

    _ROW_PREFIX = 100
    _COL_PREFIX = 200

    @staticmethod
    def from_row(x: int) -> int:
        return StimulusHelper._ROW_PREFIX + x

    @staticmethod
    def to_row(x: int) -> int:
        return x - StimulusHelper._ROW_PREFIX

    @staticmethod
    def from_col(x: int) -> int:
        return StimulusHelper._COL_PREFIX + x

    @staticmethod
    def to_col(x: int) -> int:
        return x - StimulusHelper._COL_PREFIX

    @staticmethod
    def is_col(x: int) -> bool:
        return x >= StimulusHelper._COL_PREFIX

    @staticmethod
    def is_row(x: int) -> bool:
        return not StimulusHelper.is_col(x)

    @staticmethod
    def get_train_event_id() -> dict:
        return dict(Target=StimulusHelper.TARGET, NonTarget=StimulusHelper.NON_TARGET)

    @staticmethod
    def get_prediction_event_id() -> dict:
        event_id = dict()
        for i in range(StimulusHelper._ROW_PREFIX, StimulusHelper._ROW_PREFIX + GRID_SIZE):
            event_id['row_' + str(i)] = i

        for i in range(StimulusHelper._COL_PREFIX, StimulusHelper._COL_PREFIX + GRID_SIZE):
            event_id['col_' + str(i)] = i

        return event_id


@dataclass
class Stimulus:
    type: int
    time: float = field(default_factory=lambda: time.time())
