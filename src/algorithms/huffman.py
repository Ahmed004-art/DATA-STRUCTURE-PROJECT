"""Huffman coding algorithm using a min-heap priority queue."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Mapping

from src.utils.validators import ValidationError

ASSIGNMENT_HUFFMAN_FREQUENCIES: dict[str, int] = {
    "a": 2,
    "b": 4,
    "c": 8,
    "d": 16,
    "e": 16,
}


@dataclass(order=False)
class HuffmanNode:
    """Node in a Huffman binary tree."""

    frequency: int
    symbol: str | None = None
    left: HuffmanNode | None = None
    right: HuffmanNode | None = None
    order_id: int = 0
    label: str = field(default="", init=False)

    def __post_init__(self) -> None:
        if self.symbol is not None:
            self.label = self.symbol
        elif self.left is not None and self.right is not None:
            self.label = f"({self.left.label}+{self.right.label})"

    def is_leaf(self) -> bool:
        """Return True if this node represents an input symbol."""
        return self.symbol is not None


@dataclass(frozen=True)
class HuffmanMergeStep:
    """Records a single merge operation in the Huffman priority queue."""

    step: int
    left_label: str
    left_freq: int
    right_label: str
    right_freq: int
    merged_label: str
    merged_freq: int


@dataclass(frozen=True)
class HuffmanResult:
    """Complete output of running Huffman coding on a symbol-frequency mapping."""

    frequencies: dict[str, int]
    root: HuffmanNode
    codes: dict[str, str]
    merge_steps: list[HuffmanMergeStep]
    weighted_bit_length: int


def _validate_frequencies(frequencies: Mapping[str, int]) -> dict[str, int]:
    """Validate symbol-frequency input."""
    if not frequencies:
        raise ValidationError("Frequencies mapping cannot be empty.")

    cleaned: dict[str, int] = {}
    for sym, freq in frequencies.items():
        if not isinstance(sym, str) or len(sym) != 1:
            raise ValidationError(
                f"Invalid symbol {sym!r}: each symbol must be a single character."
            )
        if isinstance(freq, bool) or not isinstance(freq, int) or freq <= 0:
            raise ValidationError(
                f"Invalid frequency for symbol {sym!r}: must be a positive integer."
            )
        cleaned[sym] = freq
    return cleaned


def build_huffman_tree(
    frequencies: Mapping[str, int],
) -> tuple[HuffmanNode, list[HuffmanMergeStep]]:
    """Construct a Huffman tree using a min-heap with deterministic tie-breaking.

    Tie-breaking key: (frequency, order_id) where initial leaves are ordered by
    insertion order, and newly merged internal nodes receive monotonically increasing
    order_ids. Left child gets bit '0' and right child gets bit '1'.

    Time Complexity:  O(k log k) where k is the number of distinct symbols.
    Space Complexity: O(k) for the priority queue and tree nodes.
    """
    validated = _validate_frequencies(frequencies)
    heap: list[tuple[int, int, HuffmanNode]] = []
    next_id = 0

    for sym, freq in validated.items():
        node = HuffmanNode(frequency=freq, symbol=sym, order_id=next_id)
        heapq.heappush(heap, (freq, next_id, node))
        next_id += 1

    merge_steps: list[HuffmanMergeStep] = []
    step_num = 1
    while len(heap) > 1:
        _, _, left = heapq.heappop(heap)
        _, _, right = heapq.heappop(heap)
        merged = HuffmanNode(
            frequency=left.frequency + right.frequency,
            symbol=None,
            left=left,
            right=right,
            order_id=next_id,
        )
        next_id += 1
        merge_steps.append(
            HuffmanMergeStep(
                step=step_num,
                left_label=left.label,
                left_freq=left.frequency,
                right_label=right.label,
                right_freq=right.frequency,
                merged_label=merged.label,
                merged_freq=merged.frequency,
            )
        )
        step_num += 1
        heapq.heappush(heap, (merged.frequency, merged.order_id, merged))

    return heap[0][2], merge_steps


def generate_huffman_codes(root: HuffmanNode) -> dict[str, str]:
    """Derive prefix-free binary codes from a Huffman tree (left='0', right='1')."""
    codes: dict[str, str] = {}

    def _walk(node: HuffmanNode, prefix: str) -> None:
        if node.is_leaf():
            assert node.symbol is not None
            codes[node.symbol] = prefix if prefix else "0"
            return
        if node.left is not None:
            _walk(node.left, prefix + "0")
        if node.right is not None:
            _walk(node.right, prefix + "1")

    _walk(root, "")
    return codes


def encode_text(text: str, codes: Mapping[str, str]) -> str:
    """Encode a string using the generated Huffman code table."""
    if not isinstance(text, str):
        raise ValidationError("Text to encode must be a string.")
    encoded_parts: list[str] = []
    for ch in text:
        if ch not in codes:
            raise ValidationError(
                f"Symbol '{ch}' is not in the Huffman code table {sorted(codes)}."
            )
        encoded_parts.append(codes[ch])
    return "".join(encoded_parts)


def decode_bits(bitstring: str, root: HuffmanNode) -> str:
    """Decode a Huffman-encoded bitstring back to the original text."""
    if not bitstring:
        return ""
    if root.is_leaf():
        assert root.symbol is not None
        if any(bit != "0" for bit in bitstring):
            raise ValidationError("Invalid bitstring for single-symbol Huffman tree.")
        return root.symbol * len(bitstring)

    decoded: list[str] = []
    current = root
    for bit in bitstring:
        if bit == "0":
            assert current.left is not None
            current = current.left
        elif bit == "1":
            assert current.right is not None
            current = current.right
        else:
            raise ValidationError(f"Invalid bit '{bit}' in bitstring.")

        if current.is_leaf():
            assert current.symbol is not None
            decoded.append(current.symbol)
            current = root

    if current is not root:
        raise ValidationError("Incomplete Huffman bitstring: ended mid-codeword.")
    return "".join(decoded)


def calculate_weighted_length(
    frequencies: Mapping[str, int], codes: Mapping[str, str]
) -> int:
    """Compute total encoded file bit length: sum(freq[s] * len(code[s]))."""
    return sum(freq * len(codes[sym]) for sym, freq in frequencies.items())


def solve_huffman(
    frequencies: Mapping[str, int] = ASSIGNMENT_HUFFMAN_FREQUENCIES,
) -> HuffmanResult:
    """Run the full Huffman coding pipeline on the given frequency table."""
    validated = _validate_frequencies(frequencies)
    root, merge_steps = build_huffman_tree(validated)
    codes = generate_huffman_codes(root)
    ordered_codes = {sym: codes[sym] for sym in validated}
    weighted_len = calculate_weighted_length(validated, ordered_codes)
    return HuffmanResult(
        frequencies=validated,
        root=root,
        codes=ordered_codes,
        merge_steps=merge_steps,
        weighted_bit_length=weighted_len,
    )
