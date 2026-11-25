"""Reusable BinaryTree and TreeNode data structures."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class TreeNode(Generic[T]):
    """A single node in a binary tree."""

    value: T
    left: TreeNode[T] | None = None
    right: TreeNode[T] | None = None


class BinaryTree(Generic[T]):
    """Binary tree container with level-order construction and structural helpers."""

    def __init__(self, root: TreeNode[T] | None = None) -> None:
        self.root = root

    def is_empty(self) -> bool:
        """Return True if the tree has no nodes."""
        return self.root is None

    def node_count(self) -> int:
        """Count total nodes in the tree via BFS. O(n) time, O(n) space."""
        if self.root is None:
            return 0
        count = 0
        queue: deque[TreeNode[T]] = deque([self.root])
        while queue:
            node = queue.popleft()
            count += 1
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return count

    @classmethod
    def from_level_order(cls, values: Sequence[T]) -> BinaryTree[T]:
        """Build a complete binary tree from a level-order sequence of values."""
        if not values:
            return cls(None)

        nodes = [TreeNode(value=v) for v in values]
        for idx in range(len(nodes)):
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            if left_idx < len(nodes):
                nodes[idx].left = nodes[left_idx]
            if right_idx < len(nodes):
                nodes[idx].right = nodes[right_idx]
        return cls(nodes[0])


def build_assignment_binary_tree() -> BinaryTree[int]:
    """Reproduce the exact 31-node complete binary tree from PDF Page 2 (1..31)."""
    return BinaryTree.from_level_order(list(range(1, 32)))
