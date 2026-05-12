from __future__ import annotations

from src.metrics.collector import MetricsCollector
from src.nodes.node import Node
from src.routing.epidemic import EpidemicRouter


class ProphetRouter(EpidemicRouter):
    def __init__(
        self,
        metrics: MetricsCollector,
        verbose: bool = False,
        p_init: float = 0.75,
        beta: float = 0.25,
        gamma: float = 0.98,
    ) -> None:
        super().__init__(metrics=metrics, verbose=verbose)
        self.p_init = p_init
        self.beta = beta
        self.gamma = gamma

    def on_contact(self, node_a: Node, node_b: Node, time: float) -> list[str]:
        node_a.clock = time
        node_b.clock = time
        self.metrics.record_contact()

        logs = [f"[{node_a.id}] contato PROPHET com {node_b.id} em t={time:.1f}"]
        self._age_probabilities(node_a, time)
        self._age_probabilities(node_b, time)
        self._increase_direct_probability(node_a, node_b)
        self._increase_direct_probability(node_b, node_a)
        self._apply_transitivity(node_a, node_b)
        self._apply_transitivity(node_b, node_a)

        summary_a = node_a.summary()
        summary_b = node_b.summary()
        send_a_to_b = [
            message
            for message in node_a.buffer.values()
            if (
                message.id not in summary_b
                and message.can_forward
                and self._should_forward(node_a, node_b, message.destination_id)
            )
        ]
        send_b_to_a = [
            message
            for message in node_b.buffer.values()
            if (
                message.id not in summary_a
                and message.can_forward
                and self._should_forward(node_b, node_a, message.destination_id)
            )
        ]

        for message in send_a_to_b:
            logs.extend(self._transfer(message, node_a, node_b, time))
        for message in send_b_to_a:
            logs.extend(self._transfer(message, node_b, node_a, time))

        return logs

    def _increase_direct_probability(self, current: Node, peer: Node) -> None:
        current.delivery_probabilities[current.id] = 1.0
        peer.delivery_probabilities[peer.id] = 1.0

        old_direct = current.delivery_probabilities.get(peer.id, 0.0)
        current.delivery_probabilities[peer.id] = old_direct + (1.0 - old_direct) * self.p_init

    def _apply_transitivity(self, current: Node, peer: Node) -> None:
        current_to_peer = current.delivery_probability(peer.id)
        for destination_id, peer_probability in peer.delivery_probabilities.items():
            if destination_id == current.id:
                continue
            old_probability = current.delivery_probabilities.get(destination_id, 0.0)
            transitive = current_to_peer * peer_probability * self.beta
            current.delivery_probabilities[destination_id] = (
                old_probability + (1.0 - old_probability) * transitive
            )

    def _age_probabilities(self, node: Node, time: float) -> None:
        elapsed = max(0.0, time - node.last_probability_update)
        if elapsed == 0:
            return

        decay = self.gamma**elapsed
        for destination_id in list(node.delivery_probabilities):
            if destination_id == node.id:
                node.delivery_probabilities[destination_id] = 1.0
            else:
                node.delivery_probabilities[destination_id] *= decay
        node.last_probability_update = time

    def _should_forward(self, sender: Node, receiver: Node, destination_id: int) -> bool:
        return receiver.delivery_probability(destination_id) > sender.delivery_probability(destination_id)
