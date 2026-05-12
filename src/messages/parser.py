from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from src.messages.message import Message


class MessageParserError(ValueError):
    pass


def parse_messages(path: str | Path, ttl_default: int = 5) -> list[Message]:
    source_sequences: defaultdict[int, int] = defaultdict(int)
    messages: list[Message] = []

    for line_number, raw_line in enumerate(Path(path).read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in line.split(",", maxsplit=4)]
        if len(parts) < 4:
            raise MessageParserError(
                f"{path}:{line_number}: expected 'tempo, origem, destino, ttl, payload'"
            )

        try:
            created_at = float(parts[0])
            source_id = int(parts[1])
            destination_id = int(parts[2])
            ttl = int(parts[3]) if parts[3] else ttl_default
        except ValueError as exc:
            raise MessageParserError(f"{path}:{line_number}: invalid message fields") from exc

        if created_at < 0:
            raise MessageParserError(f"{path}:{line_number}: message time cannot be negative")
        if ttl < 0:
            raise MessageParserError(f"{path}:{line_number}: ttl cannot be negative")
        if source_id <= 0 or destination_id <= 0:
            raise MessageParserError(f"{path}:{line_number}: node IDs must be positive")

        payload = parts[4] if len(parts) == 5 else ""
        source_sequences[source_id] += 1
        message_id = f"m-{source_id}-{source_sequences[source_id]:04d}"
        messages.append(
            Message(
                id=message_id,
                source_id=source_id,
                destination_id=destination_id,
                payload=payload,
                created_at=created_at,
                ttl=ttl,
                path=[source_id],
            )
        )

    return sorted(messages, key=lambda message: message.created_at)

