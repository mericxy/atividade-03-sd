from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_report(report: dict[str, Any], path: str | Path) -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))


def format_summary(report: dict[str, Any]) -> str:
    average_latency = report["average_latency"]
    overhead = report["overhead"]
    latency_text = "n/a" if average_latency is None else f"{average_latency:.2f}s"
    overhead_text = "n/a" if overhead is None else f"{overhead:.2f}"

    return "\n".join(
        [
            "Relatório da Simulação DTN P2P",
            "==============================",
            f"Cenário: {report['scenario']}",
            f"Roteador: {report['router']}",
            f"Nós: {report['nodes']}",
            f"Mensagens criadas: {report['total_created']}",
            f"Contatos processados: {report['contacts_processed']}",
            f"Entregas únicas: {report['unique_deliveries']}",
            f"Taxa de entrega: {report['delivery_rate'] * 100:.2f}%",
            f"Latência média: {latency_text}",
            f"Transmissões totais: {report['total_transmissions']}",
            f"Overhead: {overhead_text}",
        ]
    )
