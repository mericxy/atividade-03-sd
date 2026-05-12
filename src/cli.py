from __future__ import annotations

import argparse
import sys

from src.contacts.parser import ContactParserError
from src.messages.parser import MessageParserError
from src.metrics.report import format_summary, write_json_report
from src.simulation.engine import SimulationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador DTN P2P com roteamento epidêmico ou PROPHET")
    subparsers = parser.add_subparsers(dest="command")

    simulate = subparsers.add_parser("simulate", help="executa uma simulação completa")
    simulate.add_argument("--contacts", required=True, help="arquivo contacts.txt")
    simulate.add_argument("--messages", required=True, help="arquivo messages.txt")
    simulate.add_argument("--report", help="caminho opcional para relatório JSON")
    simulate.add_argument("--ttl-default", type=int, default=5, help="TTL padrão")
    simulate.add_argument("--scenario", help="nome do cenário no relatório")
    simulate.add_argument(
        "--router",
        choices=["epidemic", "prophet"],
        default="epidemic",
        help="algoritmo de roteamento",
    )
    simulate.add_argument(
        "--log-level",
        choices=["quiet", "info", "debug"],
        default="info",
        help="nível de log no terminal",
    )

    send = subparsers.add_parser("send", help="formata uma mensagem para messages.txt")
    send.add_argument("--time", type=float, default=0.0, help="tempo simulado de criação")
    send.add_argument("--from", dest="source_id", type=int, required=True, help="nó origem")
    send.add_argument("--to", dest="destination_id", type=int, required=True, help="nó destino")
    send.add_argument("--ttl", type=int, default=5, help="TTL da mensagem")
    send.add_argument("--msg", required=True, help="conteúdo da mensagem")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "send":
        print(f"{args.time}, {args.source_id}, {args.destination_id}, {args.ttl}, {args.msg}")
        return 0

    if args.command != "simulate":
        parser.print_help()
        return 1

    try:
        engine = SimulationEngine.from_files(
            contacts_path=args.contacts,
            messages_path=args.messages,
            ttl_default=args.ttl_default,
            scenario=args.scenario,
            router_name=args.router,
            verbose=args.log_level == "debug",
        )
        report = engine.run()
    except (ContactParserError, MessageParserError, FileNotFoundError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"erro de validação: {exc}", file=sys.stderr)
        return 3

    if args.log_level == "debug":
        print("\n".join(engine.logs))
        print()
    elif args.log_level == "info":
        for line in engine.logs:
            if "entregue" in line or line.startswith("[sim]"):
                print(line)
        if engine.logs:
            print()

    print(format_summary(report))
    if args.report:
        write_json_report(report, args.report)
        print(f"\nRelatório JSON salvo em: {args.report}")

    return 0
