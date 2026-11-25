"""Binary tree traversal algorithms (Pre-order, In-order, Post-order, Level-order)."""

from __future__ import annotations

from collections import deque
from typing import TypeVar

from src.data_structures.binary_tree import BinaryTree, TreeNode

T = TypeVar("T")


def preorder_traversal(tree: BinaryTree[T]) -> list[T]:
    """Visit nodes in Root -> Left -> Right order.

    Time Complexity:  O(n) — visits every node once.
    Space Complexity: O(h) — recursion stack depth (O(log n) balanced, O(n) skewed).
    """
    result: list[T] = []

    def _visit(node: TreeNode[T] | None) -> None:
        if node is None:
            return
        result.append(node.value)
        _visit(node.left)
        _visit(node.right)

    _visit(tree.root)
    return result


def inorder_traversal(tree: BinaryTree[T]) -> list[T]:
    """Visit nodes in Left -> Root -> Right order.

    Time Complexity:  O(n) — visits every node once.
    Space Complexity: O(h) — recursion stack depth (O(log n) balanced, O(n) skewed).
    """
    result: list[T] = []

    def _visit(node: TreeNode[T] | None) -> None:
        if node is None:
            return
        _visit(node.left)
        result.append(node.value)
        _visit(node.right)

    _visit(tree.root)
    return result


def postorder_traversal(tree: BinaryTree[T]) -> list[T]:
    """Visit nodes in Left -> Right -> Root order.

    Time Complexity:  O(n) — visits every node once.
    Space Complexity: O(h) — recursion stack depth (O(log n) balanced, O(n) skewed).
    """
    result: list[T] = []

    def _visit(node: TreeNode[T] | None) -> None:
        if node is None:
            return
        _visit(node.left)
        _visit(node.right)
        result.append(node.value)

    _visit(tree.root)
    return result


def levelorder_traversal(tree: BinaryTree[T]) -> list[T]:
    """Visit nodes level by level from top to bottom using a FIFO queue.

    Time Complexity:  O(n) — enqueues and dequeues every node once.
    Space Complexity: O(w) — maximum tree width in the queue (O(n) for complete tree).
    """
    if tree.root is None:
        return []

    result: list[T] = []
    queue: deque[TreeNode[T]] = deque([tree.root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


def all_traversals(tree: BinaryTree[T]) -> dict[str, list[T]]:
    """Compute all four standard traversals for the given binary tree."""
    return {
        "Pre-order": preorder_traversal(tree),
        "In-order": inorder_traversal(tree),
        "Post-order": postorder_traversal(tree),
        "Level-order": levelorder_traversal(tree),
    }
