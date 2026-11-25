"""Automated tests for the Stack data structure and applications."""

from __future__ import annotations

import pytest

from src.data_structures.stack import (
    Stack,
    StackUnderflowError,
    is_balanced_parentheses,
    reverse_string_with_stack,
)


def test_empty_stack_properties() -> None:
    stack: Stack[int] = Stack()
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0
    assert bool(stack) is False
    assert stack.display() == "[Empty Stack]"


def test_push_one_item() -> None:
    stack: Stack[str] = Stack()
    stack.push("A")
    assert stack.is_empty() is False
    assert stack.size() == 1
    assert stack.peek() == "A"
    assert "A" in stack.display()


def test_push_multiple_items_and_lifo_order() -> None:
    stack: Stack[int] = Stack()
    for item in (10, 20, 30, 40):
        stack.push(item)

    assert stack.size() == 4
    assert stack.to_list() == [10, 20, 30, 40]
    assert stack.pop() == 40
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10
    assert stack.is_empty() is True


def test_peek_does_not_remove_item() -> None:
    stack: Stack[str] = Stack(["bottom", "top"])
    assert stack.size() == 2
    assert stack.peek() == "top"
    assert stack.peek() == "top"
    assert stack.size() == 2


def test_size_tracking_across_operations() -> None:
    stack: Stack[int] = Stack()
    assert stack.size() == 0
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2
    stack.pop()
    assert stack.size() == 1
    stack.push(3)
    assert stack.size() == 2
    stack.pop()
    stack.pop()
    assert stack.size() == 0


def test_underflow_handling_on_pop_and_peek() -> None:
    stack: Stack[int] = Stack()
    with pytest.raises(StackUnderflowError, match="cannot pop"):
        stack.pop()
    with pytest.raises(StackUnderflowError, match="cannot peek"):
        stack.peek()


def test_practical_stack_applications() -> None:
    assert reverse_string_with_stack("Hanoi") == "ionaH"
    assert reverse_string_with_stack("") == ""
    assert is_balanced_parentheses("{[()]}") is True
    assert is_balanced_parentheses("([)]") is False
    assert is_balanced_parentheses("(((") is False
