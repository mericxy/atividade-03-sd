from __future__ import annotations

import heapq
from pathlib import Path

from src.contacts.controller import ContactEvent
from src.contacts.parser import parse_contacts
from src.messages.message import Message
from src.messages.parser import parse_messages
from src.metrics.collector import MetricsCollector
from src.nodes.node import Node
from src.routing.epidemic import EpidemicRouter
from src.routing.prophet import ProphetRouter
from src.simulation.event import EventType, SimulationEvent


class SimulationEngine:
    def __init__(
        self,
        contacts: list[ContactEvent],
        messages: list[Message],
        scenario: str = "simulation",
        router_name: str = "epidemic",
        verbose: bool = False,
    ) -> None:
        self.contacts = contacts
        self.messages = messages
        self.router_name = router_name
        self.verbose = verbose
        self.metrics = MetricsCollector(scenario=scenario, router=router_name)
        self.nodes: dict[int, Node] = {}
        self.events: list[SimulationEvent] = []
        self.logs: list[str] = []
        self.router = self._create_router(router_name)

        self._create_nodes()
        self._schedule_events()

    @classmethod
    def from_files(
        cls,
        contacts_path: str | Path,
        messages_path: str | Path,
        ttl_default: int = 5,
        scenario: str | None = None,
        router_name: str = "epidemic",
        verbose: bool = False,
    ) -> "SimulationEngine":
        contacts = parse_contacts(contacts_path)
        messages = parse_messages(messages_path, ttl_default=ttl_default)
        if scenario is None:
            scenario = Path(contacts_path).parent.name
        return cls(
            contacts=contacts,
            messages=messages,
            scenario=scenario,
            router_name=router_name,
            verbose=verbose,
        )

    def run(self) -> dict:
        while self.events:
            event = heapq.heappop(self.events)
            if event.event_type == EventType.MESSAGE_INJECTION:
                self._inject_message(event.payload, event.time)
            elif event.event_type == EventType.CONTACT_START:
                self._run_contact(event.payload, event.time)

        return self.metrics.as_dict(nodes_count=len(self.nodes))

    def _create_nodes(self) -> None:
        node_ids: set[int] = set()
        for contact in self.contacts:
            node_ids.add(contact.node_a)
            node_ids.add(contact.node_b)
        for message in self.messages:
            node_ids.add(message.source_id)
            node_ids.add(message.destination_id)

        self.nodes = {node_id: Node(id=node_id) for node_id in sorted(node_ids)}
        for node in self.nodes.values():
            node.delivery_probabilities[node.id] = 1.0

    def _create_router(self, router_name: str):
        if router_name == "epidemic":
            return EpidemicRouter(metrics=self.metrics, verbose=self.verbose)
        if router_name == "prophet":
            return ProphetRouter(metrics=self.metrics, verbose=self.verbose)
        raise ValueError(f"unknown router: {router_name}")

    def _schedule_events(self) -> None:
        for message in self.messages:
            heapq.heappush(
                self.events,
                SimulationEvent(
                    time=message.created_at,
                    priority=1,
                    event_type=EventType.MESSAGE_INJECTION,
                    payload=message,
                ),
            )

        for contact in self.contacts:
            heapq.heappush(
                self.events,
                SimulationEvent(
                    time=contact.start_time,
                    priority=2,
                    event_type=EventType.CONTACT_START,
                    payload=contact,
                ),
            )

    def _inject_message(self, message: Message, time: float) -> None:
        origin = self.nodes[message.source_id]
        origin.clock = time
        origin.store_initial(message)
        self.metrics.record_created(message)
        self.logs.append(
            f"[sim] t={time:.1f} criada {message.id} origem={message.source_id} "
            f"destino={message.destination_id} ttl={message.ttl}"
        )

        if message.source_id == message.destination_id:
            message.delivered_at = time
            origin.delivered_messages.add(message.id)
            self.metrics.record_delivery(message, time)

    def _run_contact(self, contact: ContactEvent, time: float) -> None:
        node_a = self.nodes[contact.node_a]
        node_b = self.nodes[contact.node_b]
        self.logs.extend(self.router.on_contact(node_a, node_b, time))
