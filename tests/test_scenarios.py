from __future__ import annotations

import unittest
from pathlib import Path

from src.simulation.engine import SimulationEngine


ROOT = Path(__file__).resolve().parents[1]


class ScenarioTests(unittest.TestCase):
    def run_scenario(self, name: str) -> dict:
        scenario_dir = ROOT / "docs" / "cenarios" / name
        engine = SimulationEngine.from_files(
            contacts_path=scenario_dir / "contacts.txt",
            messages_path=scenario_dir / "messages.txt",
        )
        return engine.run()

    def test_dense_scenario_delivers_all_messages(self) -> None:
        report = self.run_scenario("denso")

        self.assertEqual(report["total_created"], 4)
        self.assertEqual(report["unique_deliveries"], 4)
        self.assertEqual(report["delivery_rate"], 1.0)

    def test_sparse_scenario_keeps_some_latency_pressure(self) -> None:
        report = self.run_scenario("esparso")

        self.assertEqual(report["total_created"], 4)
        self.assertLess(report["delivery_rate"], 1.0)
        self.assertGreater(report["average_latency"], 10.0)

    def test_chain_scenario_uses_intermediate_nodes(self) -> None:
        report = self.run_scenario("cadeia")
        delivered_paths = [
            message["path"]
            for message in report["messages"]
            if message["status"] == "delivered"
        ]

        self.assertIn([1, 2, 3, 4], delivered_paths)
        self.assertEqual(report["unique_deliveries"], 2)


if __name__ == "__main__":
    unittest.main()

