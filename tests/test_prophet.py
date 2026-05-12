from __future__ import annotations

import unittest

from src.contacts.controller import ContactEvent
from src.messages.message import Message
from src.simulation.engine import SimulationEngine


class ProphetRouterTests(unittest.TestCase):
    def test_prophet_uses_contact_history_to_forward(self) -> None:
        contacts = [
            ContactEvent(1.0, 2.0, 2, 3),
            ContactEvent(2.0, 3.0, 1, 2),
            ContactEvent(3.0, 4.0, 2, 3),
        ]
        messages = [
            Message(
                id="m-1-0001",
                source_id=1,
                destination_id=3,
                payload="historico",
                created_at=0.0,
                ttl=3,
                path=[1],
            )
        ]

        report = SimulationEngine(
            contacts,
            messages,
            scenario="prophet-test",
            router_name="prophet",
        ).run()

        self.assertEqual(report["router"], "prophet")
        self.assertEqual(report["unique_deliveries"], 1)
        self.assertEqual(report["messages"][0]["path"], [1, 2, 3])

    def test_prophet_does_not_forward_without_better_probability(self) -> None:
        contacts = [ContactEvent(1.0, 2.0, 1, 2)]
        messages = [
            Message(
                id="m-1-0001",
                source_id=1,
                destination_id=3,
                payload="sem historico",
                created_at=0.0,
                ttl=3,
                path=[1],
            )
        ]

        report = SimulationEngine(
            contacts,
            messages,
            scenario="prophet-test",
            router_name="prophet",
        ).run()

        self.assertEqual(report["unique_deliveries"], 0)
        self.assertEqual(report["total_transmissions"], 0)


if __name__ == "__main__":
    unittest.main()

