import time
from dataclasses import dataclass, field


class StimulusHelper:
    C3 = 1
    C4 = 2
    C5 = 3
    C6 = 4
    C7 = 5

    @staticmethod
    def getId(val) -> int:
        kv = {
            'C3': 1,
            'C4': 2,
            'C5': 3,
            'C6': 4,
            'C7': 5
        }
        return kv[val]

    @staticmethod
    def get_train_event_id() -> dict:
        return dict(C3=StimulusHelper.C3, C4=StimulusHelper.C4, C5=StimulusHelper.C5, C6=StimulusHelper.C6, C7=StimulusHelper.C7)


@dataclass
class Stimulus:
    type: int
    time: float = field(default_factory=lambda: time.time())
