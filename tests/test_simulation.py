from __future__ import annotations

import unittest

from src.contacts.controller import ContactEvent
from src.messages.message import Message
from src.simulation.engine import SimulationEngine


class SimulationTests(unittest.TestCase):
    def test_chain_delivers_message_by_store_and_forward(self) -> None:
        contacts = [
            ContactEvent(1.0, 2.0, 1, 2),
            ContactEvent(4.0, 5.0, 2, 3),
            ContactEvent(8.0, 9.0, 3, 4),
        ]
        messages = [
            Message(
                id="m-1-0001",
                source_id=1,
                destination_id=4,
                payload="ola",
                created_at=0.0,
                ttl=4,
                path=[1],
            )
        ]

        report = SimulationEngine(contacts, messages, scenario="test").run()

        self.assertEqual(report["unique_deliveries"], 1)
        self.assertEqual(report["delivery_rate"], 1.0)
        self.assertEqual(report["messages"][0]["path"], [1, 2, 3, 4])
        self.assertEqual(report["total_transmissions"], 3)

    def test_ttl_zero_prevents_forwarding(self) -> None:
        contacts = [
            ContactEvent(1.0, 2.0, 1, 2),
            ContactEvent(4.0, 5.0, 2, 3),
        ]
        messages = [
            Message(
                id="m-1-0001",
                source_id=1,
                destination_id=3,
                payload="ola",
                created_at=0.0,
                ttl=1,
                path=[1],
            )
        ]

        report = SimulationEngine(contacts, messages, scenario="test").run()

        self.assertEqual(report["unique_deliveries"], 0)
        self.assertEqual(report["total_transmissions"], 1)
        self.assertIsNone(report["overhead"])

    def test_same_time_message_is_available_for_contact(self) -> None:
        contacts = [ContactEvent(0.0, 1.0, 1, 2)]
        messages = [
            Message(
                id="m-1-0001",
                source_id=1,
                destination_id=2,
                payload="instantanea",
                created_at=0.0,
                ttl=1,
                path=[1],
            )
        ]

        report = SimulationEngine(contacts, messages, scenario="test").run()

        self.assertEqual(report["unique_deliveries"], 1)
        self.assertEqual(report["average_latency"], 0.0)


if __name__ == "__main__":
    unittest.main()

