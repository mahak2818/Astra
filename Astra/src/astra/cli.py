"""
Command Line Interface (CLI) for Astra Personal AI Operating Runtime.
"""

import argparse
import sys
import json
from typing import List

from astra import __version__
from astra.config.config import get_config
from astra.runtime.engine import AstraEngine
from astra.models.schemas import UserConfirmationRequest


def cli_confirmation_callback(request: UserConfirmationRequest) -> bool:
    """CLI user confirmation prompt for Level 2 actions."""
    print(f"\n[SECURITY WARNING - LEVEL 2 CLEARANCE REQUIRED]")
    print(f"Action: {request.capability_name}.{request.action_name}")
    print(f"Description: {request.description}")
    response = input("Do you grant approval to execute this action? (y/N): ").strip().lower()
    return response == 'y'


def main(args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="astra", description="Astra: Personal AI Operating Layer and Runtime")
    parser.add_argument("--version", "-v", action="version", version=f"Astra v{__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Execute a natural language request")
    run_parser.add_argument("query", nargs="+", help="Natural language request for Astra")
    run_parser.add_argument("--auto-approve", action="store_true", help="Auto approve Level 2 security actions")

    # Command: status
    subparsers.add_parser("status", help="Display system status and configuration")

    # Command: capabilities
    subparsers.add_parser("capabilities", help="List all registered capabilities")

    # Command: memory
    mem_parser = subparsers.add_parser("memory", help="Inspect memory records")
    mem_parser.add_argument("--tier", choices=["profile", "working", "project", "long_term", "execution"], default="execution")

    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        sys.exit(0)

    config = get_config()

    if parsed_args.command == "status":
        print("--- Astra Personal AI Runtime Status ---")
        print(f"Version: {__version__}")
        print(f"Environment: {config.environment}")
        print(f"Data Dir: {config.data_dir}")
        print(f"Database Path: {config.db_path}")
        print(f"Default Model: {config.default_model}")
        print("Status: Active & Operational")

    elif parsed_args.command == "capabilities":
        engine = AstraEngine()
        print("--- Registered Astra Capabilities ---")
        for name, cap in engine.capability_registry.list_all().items():
            print(f"- {name}: Class {cap.__class__.__name__}")

    elif parsed_args.command == "run":
        raw_query = " ".join(parsed_args.query)
        callback = (lambda r: True) if parsed_args.auto_approve else cli_confirmation_callback
        engine = AstraEngine(confirmation_callback=callback)
        res = engine.execute_request(raw_query)
        print("\n--- Astra Execution Summary ---")
        print(json.dumps(res, indent=2))

    elif parsed_args.command == "memory":
        engine = AstraEngine()
        items = engine.memory_manager.list_memories(category=parsed_args.tier, limit=10)
        print(f"--- Astra Memory Tier: {parsed_args.tier} ({len(items)} records) ---")
        for idx, item in enumerate(items, 1):
            print(f"{idx}. [{item.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Key: {item.key} | Content: {item.content}")


if __name__ == "__main__":
    main()
