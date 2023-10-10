import time
from dataclasses import dataclass, field

@dataclass
class Stimulus:
    type: int
    time: float = field(default_factory=lambda: time.time())
