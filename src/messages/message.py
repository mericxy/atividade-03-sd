from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(slots=True)
class Message:
    id: str
    source_id: int
    destination_id: int
    payload: str
    created_at: float
    ttl: int
    hop_count: int = 0
    delivered_at: float | None = None
    path: list[int] = field(default_factory=list)

    def copy_for_receiver(self, receiver_id: int) -> "Message":
        return replace(
            self,
            ttl=self.ttl - 1,
            hop_count=self.hop_count + 1,
            path=[*self.path, receiver_id],
        )

    @property
    def can_forward(self) -> bool:
        return self.ttl > 0

