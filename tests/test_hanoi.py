"""Automated tests for the recursive Tower of Hanoi implementation."""

from __future__ import annotations

import pytest

from src.algorithms.hanoi import (
    HanoiMove,
    IllegalHanoiMoveError,
    expected_hanoi_moves,
    solve_tower_of_hanoi,
    verify_hanoi_moves,
)
from src.utils.validators import ValidationError


@pytest.mark.parametrize("disks", [1, 2, 3, 4])
def test_hanoi_move_counts_and_legal_sequences(disks: int) -> None:
    moves = solve_tower_of_hanoi(disks)
    expected = (1 << disks) - 1
    assert len(moves) == expected
    assert expected_hanoi_moves(disks) == expected
    assert verify_hanoi_moves(disks, moves) is True


def test_hanoi_three_disks_exact_sequence() -> None:
    moves = solve_tower_of_hanoi(3, source="A", auxiliary="B", destination="C")
    tuples = [(m.disk, m.source, m.destination) for m in moves]
    assert tuples == [
        (1, "A", "C"),
        (2, "A", "B"),
        (1, "C", "B"),
        (3, "A", "C"),
        (1, "B", "A"),
        (2, "B", "C"),
        (1, "A", "C"),
    ]
    assert verify_hanoi_moves(3, moves, source="A", auxiliary="B", destination="C") is True


def test_hanoi_custom_rod_names_and_string_input() -> None:
    moves = solve_tower_of_hanoi("2", source="Left", auxiliary="Mid", destination="Right")
    assert len(moves) == 3
    assert all(m.source in {"Left", "Mid", "Right"} for m in moves)
    assert all(m.destination in {"Left", "Mid", "Right"} for m in moves)
    assert verify_hanoi_moves(2, moves, source="Left", auxiliary="Mid", destination="Right") is True


def test_hanoi_rejects_illegal_disk_placement() -> None:
    illegal_moves = [
        HanoiMove(step=1, disk=1, source="Source", destination="Destination"),
        HanoiMove(step=2, disk=2, source="Source", destination="Destination"),
    ]
    with pytest.raises(IllegalHanoiMoveError, match="smaller disk"):
        verify_hanoi_moves(2, illegal_moves)


@pytest.mark.parametrize("invalid_input", [0, -1, -5, "0", "-3", "abc", "", "2.5", True])
def test_hanoi_invalid_inputs(invalid_input: object) -> None:
    with pytest.raises(ValidationError):
        solve_tower_of_hanoi(invalid_input)  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        expected_hanoi_moves(invalid_input)  # type: ignore[arg-type]
