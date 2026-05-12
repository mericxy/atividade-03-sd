from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.contacts.parser import ContactParserError, parse_contacts
from src.messages.parser import MessageParserError, parse_messages


class ParserTests(unittest.TestCase):
    def test_parse_contacts_ignores_comments_and_sorts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "contacts.txt"
            path.write_text(
                "\n".join(
                    [
                        "# tempo_inicio, tempo_fim, noA, noB",
                        "5.0, 6.0, 2, 3",
                        "1.0, 2.0, 1, 2",
                    ]
                )
            )

            contacts = parse_contacts(path)

        self.assertEqual([contact.start_time for contact in contacts], [1.0, 5.0])
        self.assertEqual((contacts[0].node_a, contacts[0].node_b), (1, 2))

    def test_parse_contacts_rejects_invalid_interval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "contacts.txt"
            path.write_text("3.0, 2.0, 1, 2")

            with self.assertRaises(ContactParserError):
                parse_contacts(path)

    def test_parse_messages_generates_ids_and_preserves_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "messages.txt"
            path.write_text("0.0, 1, 4, 5, ola, com virgula")

            messages = parse_messages(path)

        self.assertEqual(messages[0].id, "m-1-0001")
        self.assertEqual(messages[0].payload, "ola, com virgula")
        self.assertEqual(messages[0].path, [1])

    def test_parse_messages_rejects_negative_ttl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "messages.txt"
            path.write_text("0.0, 1, 4, -1, invalida")

            with self.assertRaises(MessageParserError):
                parse_messages(path)


if __name__ == "__main__":
    unittest.main()

