"""Integration tests for CLI menus, error handling, and --demo entry points."""

from __future__ import annotations

from typing import Iterator

import pytest

from main import main
from src.cli.menu import (
    main_menu,
    run_binary_tree_menu,
    run_graph_menu,
    run_hanoi_cli,
    run_huffman_demonstration,
    run_interactive_stack,
)


def _mock_inputs(responses: list[str]) -> object:
    it: Iterator[str] = iter(responses)

    def _reader(prompt: str = "") -> str:
        print(prompt, end="")
        return next(it)

    return _reader


def test_main_demo_all_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--demo", "all", "--disks", "2"])
    captured = capsys.readouterr().out
    assert exit_code == 0
    assert "Stack Data Structure Demonstration" in captured
    assert "Completed in 3 moves" in captured
    assert "Assignment 31-Node Binary Tree & Traversals" in captured
    assert "Weighted Encoded File Length (sum freq * len): 96 bits" in captured
    assert "Figure 1 Shortest Path A -> L: A -> D -> H -> E -> J -> L (Total Cost: 20)" in captured
    assert "Total MST Weight: 35" in captured
    assert "Total MST Weight: 42" in captured


def test_main_menu_navigation_and_invalid_option(capsys: pytest.CaptureFixture[str]) -> None:
    inputs = _mock_inputs(["99", "0"])
    main_menu(input_fn=inputs)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Invalid selection" in out
    assert "Exiting DCOMP320 CLI. Goodbye!" in out


def test_interactive_stack_flow_and_underflow(capsys: pytest.CaptureFixture[str]) -> None:
    inputs = _mock_inputs(["2", "3", "1", "", "1", "item1", "4", "5", "2", "9", "0"])
    run_interactive_stack(input_fn=inputs)  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "cannot pop from an empty stack" in out
    assert "cannot peek an empty stack" in out
    assert "Cannot push an empty value" in out
    assert "Pushed 'item1'" in out
    assert "Popped: 'item1'" in out
    assert "Invalid choice" in out


def test_hanoi_cli_invalid_and_large_disk_cancel(capsys: pytest.CaptureFixture[str]) -> None:
    run_hanoi_cli(input_fn=_mock_inputs(["abc"]))  # type: ignore[arg-type]
    assert "Input Error:" in capsys.readouterr().out

    run_hanoi_cli(input_fn=_mock_inputs(["11", "n"]))  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Warning: 11 disks require 2,047 moves" in out
    assert "Operation cancelled." in out


def test_binary_tree_menu_and_huffman_invalid_custom(capsys: pytest.CaptureFixture[str]) -> None:
    run_binary_tree_menu(input_fn=_mock_inputs(["1", "2", "3", "4", "9", "0"]))  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Pre-order" in out
    assert "In-order" in out
    assert "Post-order" in out
    assert "Level-order" in out
    assert "Invalid choice" in out

    run_huffman_demonstration(input_fn=_mock_inputs(["abz"]), interactive=True)  # type: ignore[arg-type]
    assert "Input Error: Symbol 'z' is not in the Huffman code table" in capsys.readouterr().out


def test_graph_menu_navigation(capsys: pytest.CaptureFixture[str]) -> None:
    run_graph_menu(input_fn=_mock_inputs(["1", "3", "8", "99", "0"]))  # type: ignore[arg-type]
    out = capsys.readouterr().out
    assert "Graph: Figure 1" in out
    assert "Figure 1 Adjacency Matrix" in out
    assert "Figure 1 Shortest Path A -> L" in out
    assert "Invalid choice" in out
