from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import count
from typing import Any


class EventType(str, Enum):
    MESSAGE_INJECTION = "message_injection"
    CONTACT_START = "contact_start"


_event_sequence = count()


@dataclass(order=True, slots=True)
class SimulationEvent:
    time: float
    priority: int
    sequence: int = field(default_factory=lambda: next(_event_sequence))
    event_type: EventType = field(compare=False, default=EventType.CONTACT_START)
    payload: Any = field(compare=False, default=None)

