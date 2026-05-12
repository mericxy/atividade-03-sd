from __future__ import annotations

from src.metrics.collector import MetricsCollector
from src.nodes.node import Node


class EpidemicRouter:
    def __init__(self, metrics: MetricsCollector, verbose: bool = False) -> None:
        self.metrics = metrics
        self.verbose = verbose

    def on_contact(self, node_a: Node, node_b: Node, time: float) -> list[str]:
        node_a.clock = time
        node_b.clock = time
        self.metrics.record_contact()

        logs = [f"[{node_a.id}] contato com {node_b.id} em t={time:.1f}"]
        summary_a = node_a.summary()
        summary_b = node_b.summary()

        send_a_to_b = [
            message
            for message in node_a.buffer.values()
            if message.id not in summary_b and message.can_forward
        ]
        send_b_to_a = [
            message
            for message in node_b.buffer.values()
            if message.id not in summary_a and message.can_forward
        ]

        for message in send_a_to_b:
            logs.extend(self._transfer(message, node_a, node_b, time))
        for message in send_b_to_a:
            logs.extend(self._transfer(message, node_b, node_a, time))

        return logs

    def _transfer(self, message, sender: Node, receiver: Node, time: float) -> list[str]:
        copied = message.copy_for_receiver(receiver.id)
        accepted = receiver.receive(copied)
        if not accepted:
            return []

        delivered = receiver.id == copied.destination_id
        if delivered:
            copied.delivered_at = time
            receiver.delivered_messages.add(copied.id)
            first_delivery = self.metrics.record_delivery(copied, time)
        else:
            first_delivery = False

        self.metrics.record_transmission(
            time=time,
            original_message=message,
            copied_message=copied,
            from_node=sender.id,
            to_node=receiver.id,
            delivered=delivered,
        )

        logs = [
            f"[{sender.id}] enviando {copied.id} para {receiver.id} ttl={message.ttl}->{copied.ttl}",
            f"[{receiver.id}] recebeu {copied.id} destino={copied.destination_id} ttl={copied.ttl}",
        ]
        if first_delivery:
            logs.append(f"[{receiver.id}] mensagem {copied.id} entregue em t={time:.1f}")
        return logs

