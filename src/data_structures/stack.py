"""Reusable LIFO Stack data structure and practical stack applications."""

from __future__ import annotations

from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class StackUnderflowError(IndexError):
    """Raised when attempting to pop or peek from an empty stack."""


class Stack(Generic[T]):
    """Last-In, First-Out (LIFO) stack backed by a Python list.

    Time Complexities:
        - push(item): O(1) amortized
        - pop():      O(1)
        - peek():     O(1)
        - is_empty(): O(1)
        - size():     O(1)
        - display():  O(n) where n is the number of items in the stack
    Space Complexity: O(n)
    """

    def __init__(self, initial_items: Iterable[T] | None = None) -> None:
        self._items: list[T] = []
        if initial_items is not None:
            for item in initial_items:
                self.push(item)

    def push(self, item: T) -> None:
        """Push an item onto the top of the stack. O(1) amortized."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item of the stack. O(1).

        Raises:
            StackUnderflowError: If the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowError("Stack underflow: cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it. O(1).

        Raises:
            StackUnderflowError: If the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowError("Stack underflow: cannot peek an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack contains no items, False otherwise. O(1)."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items currently on the stack. O(1)."""
        return len(self._items)

    def display(self) -> str:
        """Return a formatted top-to-bottom string representation of the stack. O(n)."""
        if self.is_empty():
            return "[Empty Stack]"
        lines = ["TOP ->"]
        for idx in range(len(self._items) - 1, -1, -1):
            marker = " (top)" if idx == len(self._items) - 1 else ""
            lines.append(f"  | {self._items[idx]!r} |{marker}")
        lines.append("  +-------+\n  BOTTOM")
        return "\n".join(lines)

    def to_list(self) -> list[T]:
        """Return a shallow copy of stack items from bottom to top. O(n)."""
        return list(self._items)

    def __len__(self) -> int:
        return self.size()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


def reverse_string_with_stack(text: str) -> str:
    """Reverse a string by pushing all characters onto a Stack and popping them."""
    stack: Stack[str] = Stack()
    for ch in text:
        stack.push(ch)
    reversed_chars: list[str] = []
    while not stack.is_empty():
        reversed_chars.append(stack.pop())
    return "".join(reversed_chars)


def is_balanced_parentheses(expression: str) -> bool:
    """Check whether (), [], and {} brackets in an expression are balanced."""
    matching = {")": "(", "]": "[", "}": "{"}
    openers = set(matching.values())
    stack: Stack[str] = Stack()

    for ch in expression:
        if ch in openers:
            stack.push(ch)
        elif ch in matching:
            if stack.is_empty() or stack.pop() != matching[ch]:
                return False
    return stack.is_empty()
