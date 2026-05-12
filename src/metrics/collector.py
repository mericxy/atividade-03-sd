from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any

from src.messages.message import Message


@dataclass(frozen=True, slots=True)
class TransmissionRecord:
    time: float
    message_id: str
    from_node: int
    to_node: int
    ttl_before: int
    ttl_after: int
    delivered: bool


@dataclass(frozen=True, slots=True)
class DeliveryRecord:
    message_id: str
    source_id: int
    destination_id: int
    created_at: float
    delivered_at: float
    latency: float
    path: list[int]


class MetricsCollector:
    def __init__(self, scenario: str = "simulation", router: str = "epidemic") -> None:
        self.scenario = scenario
        self.router = router
        self.total_created = 0
        self.contacts_processed = 0
        self.transmissions: list[TransmissionRecord] = []
        self.deliveries: dict[str, DeliveryRecord] = {}
        self.duplicate_deliveries = 0
        self.messages: dict[str, Message] = {}

    def record_created(self, message: Message) -> None:
        self.total_created += 1
        self.messages[message.id] = message

    def record_contact(self) -> None:
        self.contacts_processed += 1

    def record_transmission(
        self,
        time: float,
        original_message: Message,
        copied_message: Message,
        from_node: int,
        to_node: int,
        delivered: bool,
    ) -> None:
        self.transmissions.append(
            TransmissionRecord(
                time=time,
                message_id=copied_message.id,
                from_node=from_node,
                to_node=to_node,
                ttl_before=original_message.ttl,
                ttl_after=copied_message.ttl,
                delivered=delivered,
            )
        )

    def record_delivery(self, message: Message, time: float) -> bool:
        if message.id in self.deliveries:
            self.duplicate_deliveries += 1
            return False

        self.deliveries[message.id] = DeliveryRecord(
            message_id=message.id,
            source_id=message.source_id,
            destination_id=message.destination_id,
            created_at=message.created_at,
            delivered_at=time,
            latency=time - message.created_at,
            path=list(message.path),
        )
        return True

    @property
    def unique_deliveries(self) -> int:
        return len(self.deliveries)

    @property
    def total_transmissions(self) -> int:
        return len(self.transmissions)

    @property
    def delivery_rate(self) -> float:
        if self.total_created == 0:
            return 0.0
        return self.unique_deliveries / self.total_created

    @property
    def average_latency(self) -> float | None:
        if not self.deliveries:
            return None
        return mean(delivery.latency for delivery in self.deliveries.values())

    @property
    def overhead(self) -> float | None:
        if self.unique_deliveries == 0:
            return None
        return self.total_transmissions / self.unique_deliveries

    def as_dict(self, nodes_count: int) -> dict[str, Any]:
        message_rows: list[dict[str, Any]] = []
        for message_id in sorted(self.messages):
            message = self.messages[message_id]
            delivery = self.deliveries.get(message_id)
            if delivery is None:
                message_rows.append(
                    {
                        "id": message.id,
                        "source_id": message.source_id,
                        "destination_id": message.destination_id,
                        "status": "not_delivered",
                        "created_at": message.created_at,
                        "delivered_at": None,
                        "latency": None,
                        "path": list(message.path),
                    }
                )
            else:
                message_rows.append({**asdict(delivery), "status": "delivered"})

        return {
            "scenario": self.scenario,
            "router": self.router,
            "nodes": nodes_count,
            "total_created": self.total_created,
            "unique_deliveries": self.unique_deliveries,
            "delivery_rate": self.delivery_rate,
            "average_latency": self.average_latency,
            "total_transmissions": self.total_transmissions,
            "overhead": self.overhead,
            "contacts_processed": self.contacts_processed,
            "duplicate_deliveries": self.duplicate_deliveries,
            "messages": message_rows,
            "transmissions": [asdict(record) for record in self.transmissions],
        }
