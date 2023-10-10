import time
from dataclasses import dataclass, field

from p300.config import GRID_SIZE


class StimulusHelper:
    C5 = 1
    C6 = 2


@dataclass
class Stimulus:
    type: int
    time: float = field(default_factory=lambda: time.time())
