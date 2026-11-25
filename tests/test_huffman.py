"""Automated tests for the Huffman coding algorithm."""

from __future__ import annotations

import pytest

from src.algorithms.huffman import (
    ASSIGNMENT_HUFFMAN_FREQUENCIES,
    decode_bits,
    encode_text,
    solve_huffman,
)
from src.utils.validators import ValidationError


def test_huffman_assignment_codes_and_lengths() -> None:
    result = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    assert result.frequencies == {"a": 2, "b": 4, "c": 8, "d": 16, "e": 16}
    assert set(result.codes.keys()) == {"a", "b", "c", "d", "e"}
    assert len(result.merge_steps) == 4
    assert result.weighted_bit_length == 96

    encoded_abcde = encode_text("abcde", result.codes)
    assert len(encoded_abcde) == 14
    assert decode_bits(encoded_abcde, result.root) == "abcde"


def test_huffman_prefix_free_property() -> None:
    result = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    code_list = list(result.codes.values())
    for i, c1 in enumerate(code_list):
        for j, c2 in enumerate(code_list):
            if i != j:
                assert not c2.startswith(c1), f"Code {c1} is a prefix of {c2}"


def test_huffman_deterministic_across_runs() -> None:
    r1 = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    r2 = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    assert r1.codes == r2.codes
    assert r1.merge_steps == r2.merge_steps
    assert r1.weighted_bit_length == r2.weighted_bit_length


def test_huffman_encode_decode_roundtrip() -> None:
    result = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    message = "eeddccba"
    bits = encode_text(message, result.codes)
    assert decode_bits(bits, result.root) == message


def test_huffman_invalid_inputs() -> None:
    result = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)
    with pytest.raises(ValidationError, match="not in the Huffman code table"):
        encode_text("abz", result.codes)
    with pytest.raises(ValidationError):
        solve_huffman({})
    with pytest.raises(ValidationError):
        solve_huffman({"a": 0, "b": 4})
    with pytest.raises(ValidationError):
        solve_huffman({"ab": 2})
