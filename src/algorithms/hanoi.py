"""Recursive Tower of Hanoi solver and move-sequence verifier."""

from __future__ import annotations

from dataclasses import dataclass

from src.utils.validators import parse_positive_int

LARGE_DISK_WARNING_THRESHOLD = 10


class IllegalHanoiMoveError(RuntimeError):
    """Raised if a move violates Tower of Hanoi rules."""


@dataclass(frozen=True)
class HanoiMove:
    """Represents a single disk movement between two rods."""

    step: int
    disk: int
    source: str
    destination: str

    def format_move(self) -> str:
        """Return a human-readable description of this move."""
        return (
            f"Step {self.step:>3}: Move disk {self.disk} "
            f"from {self.source} -> {self.destination}"
        )


def expected_hanoi_moves(n: int | str) -> int:
    """Calculate the expected minimum number of moves (2^n - 1) for n disks."""
    disks = parse_positive_int(n, "number of disks")
    return (1 << disks) - 1


def solve_tower_of_hanoi(
    n: int | str,
    source: str = "Source",
    auxiliary: str = "Auxiliary",
    destination: str = "Destination",
) -> list[HanoiMove]:
    """Solve the Tower of Hanoi puzzle recursively for n disks.

    Time Complexity:  O(2^n) — exactly 2^n - 1 recursive disk moves.
    Space Complexity: O(n) call stack depth + O(2^n) to store the returned move list.
    """
    disks = parse_positive_int(n, "number of disks")
    if len({source, auxiliary, destination}) != 3:
        raise ValueError("Source, auxiliary, and destination rod names must be distinct.")

    moves: list[HanoiMove] = []

    def _recurse(count: int, src: str, aux: str, dst: str) -> None:
        if count == 1:
            moves.append(
                HanoiMove(step=len(moves) + 1, disk=1, source=src, destination=dst)
            )
            return
        _recurse(count - 1, src, dst, aux)
        moves.append(
            HanoiMove(step=len(moves) + 1, disk=count, source=src, destination=dst)
        )
        _recurse(count - 1, aux, src, dst)

    _recurse(disks, source, auxiliary, destination)

    expected = expected_hanoi_moves(disks)
    if len(moves) != expected:
        raise RuntimeError(
            f"Move count mismatch: expected {expected}, got {len(moves)}."
        )
    return moves


def verify_hanoi_moves(
    n: int,
    moves: list[HanoiMove],
    source: str = "Source",
    auxiliary: str = "Auxiliary",
    destination: str = "Destination",
) -> bool:
    """Simulate a sequence of HanoiMove objects to verify every rule is respected.

    Verifies:
    - Each move takes the top disk from a non-empty rod.
    - No larger disk is ever placed on top of a smaller disk.
    - Total moves equal 2^n - 1.
    - All disks end on the destination rod in strictly descending order [n, ..., 1].
    """
    disks = parse_positive_int(n, "number of disks")
    rods: dict[str, list[int]] = {
        source: list(range(disks, 0, -1)),
        auxiliary: [],
        destination: [],
    }

    for move in moves:
        if move.source not in rods or move.destination not in rods:
            raise IllegalHanoiMoveError(
                f"Invalid rod name in move: {move.source} -> {move.destination}."
            )
        if not rods[move.source]:
            raise IllegalHanoiMoveError(
                f"Step {move.step}: cannot move from empty rod '{move.source}'."
            )
        top_disk = rods[move.source][-1]
        if top_disk != move.disk:
            raise IllegalHanoiMoveError(
                f"Step {move.step}: expected top disk {top_disk} on '{move.source}', "
                f"got disk {move.disk}."
            )
        if rods[move.destination] and rods[move.destination][-1] < top_disk:
            raise IllegalHanoiMoveError(
                f"Step {move.step}: cannot place disk {top_disk} onto smaller disk "
                f"{rods[move.destination][-1]} on '{move.destination}'."
            )
        rods[move.source].pop()
        rods[move.destination].append(top_disk)

    expected_final = list(range(disks, 0, -1))
    if len(moves) != expected_hanoi_moves(disks):
        raise IllegalHanoiMoveError(
            f"Expected {expected_hanoi_moves(disks)} moves, got {len(moves)}."
        )
    if rods[destination] != expected_final or rods[source] or rods[auxiliary]:
        raise IllegalHanoiMoveError(
            f"Final rod state invalid: {rods}"
        )
    return True
