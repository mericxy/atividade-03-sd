from __future__ import annotations

from dataclasses import dataclass, field

from src.messages.message import Message


@dataclass(slots=True)
class Node:
    id: int
    clock: float = 0.0
    buffer: dict[str, Message] = field(default_factory=dict)
    seen_messages: set[str] = field(default_factory=set)
    delivered_messages: set[str] = field(default_factory=set)
    delivery_probabilities: dict[int, float] = field(default_factory=dict)
    last_probability_update: float = 0.0

    def store_initial(self, message: Message) -> bool:
        if message.id in self.seen_messages:
            return False
        self.buffer[message.id] = message
        self.seen_messages.add(message.id)
        return True

    def receive(self, message: Message) -> bool:
        if message.id in self.seen_messages:
            return False
        self.buffer[message.id] = message
        self.seen_messages.add(message.id)
        return True

    def summary(self) -> set[str]:
        return set(self.seen_messages)

    def delivery_probability(self, destination_id: int) -> float:
        if destination_id == self.id:
            return 1.0
        return self.delivery_probabilities.get(destination_id, 0.0)
