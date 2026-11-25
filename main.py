"""Application entry point for the DCOMP320 Data Structures & Algorithms project."""

from __future__ import annotations

import argparse
import sys

from src.cli.menu import (
    main_menu,
    run_binary_tree_demonstration,
    run_graph_demonstration,
    run_hanoi_cli,
    run_huffman_demonstration,
    run_stack_demonstration,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse optional CLI flags for automated or scripted execution."""
    parser = argparse.ArgumentParser(
        description="DCOMP320 Data Structures and Algorithms Terminal Application"
    )
    parser.add_argument(
        "--demo",
        choices=["m2", "m3", "m4", "all", "stack", "hanoi", "tree", "huffman", "graph"],
        help="Run a non-interactive demonstration and exit.",
    )
    parser.add_argument(
        "--disks",
        type=int,
        default=3,
        help="Number of disks to use with --demo hanoi or --demo m2 (default: 3).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Launch the requested CLI mode."""
    args = parse_args(argv)
    if args.demo == "stack":
        run_stack_demonstration()
        return 0
    if args.demo == "hanoi":
        run_hanoi_cli(default_disks=args.disks)
        return 0
    if args.demo == "m2":
        run_stack_demonstration()
        run_hanoi_cli(default_disks=args.disks)
        return 0
    if args.demo == "tree":
        run_binary_tree_demonstration("all")
        return 0
    if args.demo == "huffman":
        run_huffman_demonstration(interactive=False)
        return 0
    if args.demo == "m3":
        run_binary_tree_demonstration("all")
        run_huffman_demonstration(interactive=False)
        return 0
    if args.demo in {"m4", "graph"}:
        run_graph_demonstration("all")
        return 0
    if args.demo == "all":
        run_stack_demonstration()
        run_hanoi_cli(default_disks=args.disks)
        run_binary_tree_demonstration("all")
        run_huffman_demonstration(interactive=False)
        run_graph_demonstration("all")
        return 0

    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nSession terminated by user.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
