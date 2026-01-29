#!/usr/bin/env python3
"""
State Sentinel CLI

A unified health & determinism auditor for Godot 4.x projects.
Combines static compilation checks with headless replay verification.
"""

import argparse
import sys
from .static_audit import run_static_audit
from .replay_audit import run_replay_audit

def main():
    parser = argparse.ArgumentParser(description="State Sentinel: Godot Project Auditor")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Static Audit Command
    static_parser = subparsers.add_parser("static", help="Run static compilation checks on .gd files")
    static_parser.add_argument("--path", default=".", help="Project root directory (default: current)")
    static_parser.add_argument("--workers", type=int, default=None, help="Number of parallel workers")

    # Replay Audit Command
    replay_parser = subparsers.add_parser("replay", help="Run deterministic replay verification")
    replay_parser.add_argument("file", help="Path to .amber_replay.jsonl file")
    replay_parser.add_argument("--fastforward", action="store_true", help="Run in fast-forward mode")
    replay_parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")

    args = parser.parse_args()

    if args.command == "static":
        sys.exit(run_static_audit(args.path, args.workers))
    elif args.command == "replay":
        sys.exit(run_replay_audit(args.file, args.fastforward, args.timeout))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
