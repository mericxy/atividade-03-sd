from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContactEvent:
    start_time: float
    end_time: float
    node_a: int
    node_b: int

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

