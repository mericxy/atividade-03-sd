from __future__ import annotations

from pathlib import Path

from src.contacts.controller import ContactEvent


class ContactParserError(ValueError):
    pass


def parse_contacts(path: str | Path) -> list[ContactEvent]:
    contacts: list[ContactEvent] = []

    for line_number, raw_line in enumerate(Path(path).read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 4:
            raise ContactParserError(
                f"{path}:{line_number}: expected 'tempo_inicio, tempo_fim, noA, noB'"
            )

        try:
            start_time = float(parts[0])
            end_time = float(parts[1])
            node_a = int(parts[2])
            node_b = int(parts[3])
        except ValueError as exc:
            raise ContactParserError(f"{path}:{line_number}: invalid contact fields") from exc

        if start_time < 0 or end_time < 0:
            raise ContactParserError(f"{path}:{line_number}: contact times cannot be negative")
        if end_time < start_time:
            raise ContactParserError(f"{path}:{line_number}: end time cannot be before start time")
        if node_a <= 0 or node_b <= 0:
            raise ContactParserError(f"{path}:{line_number}: node IDs must be positive")
        if node_a == node_b:
            raise ContactParserError(f"{path}:{line_number}: contact requires two different nodes")

        contacts.append(ContactEvent(start_time, end_time, node_a, node_b))

    return sorted(contacts, key=lambda contact: (contact.start_time, contact.end_time))

