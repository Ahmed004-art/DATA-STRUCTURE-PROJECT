"""Automated tests for the 31-node Binary Tree and four traversal algorithms."""

from __future__ import annotations

from src.algorithms.traversals import (
    all_traversals,
    inorder_traversal,
    levelorder_traversal,
    postorder_traversal,
    preorder_traversal,
)
from src.data_structures.binary_tree import BinaryTree, build_assignment_binary_tree

EXPECTED_PREORDER = [
    1, 2, 4, 8, 16, 17, 9, 18, 19, 5, 10, 20, 21, 11, 22, 23,
    3, 6, 12, 24, 25, 13, 26, 27, 7, 14, 28, 29, 15, 30, 31,
]
EXPECTED_INORDER = [
    16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 23, 1,
    24, 12, 25, 6, 26, 13, 27, 3, 28, 14, 29, 7, 30, 15, 31,
]
EXPECTED_POSTORDER = [
    16, 17, 8, 18, 19, 9, 4, 20, 21, 10, 22, 23, 11, 5, 2,
    24, 25, 12, 26, 27, 13, 6, 28, 29, 14, 30, 31, 15, 7, 3, 1,
]
EXPECTED_LEVELORDER = list(range(1, 32))


def test_assignment_tree_structure_and_node_count() -> None:
    tree = build_assignment_binary_tree()
    assert tree.is_empty() is False
    assert tree.node_count() == 31
    assert tree.root is not None
    assert tree.root.value == 1
    assert tree.root.left is not None and tree.root.left.value == 2
    assert tree.root.right is not None and tree.root.right.value == 3
    assert tree.root.left.left is not None and tree.root.left.left.value == 4
    assert tree.root.left.right is not None and tree.root.left.right.value == 5
    assert tree.root.right.left is not None and tree.root.right.left.value == 6
    assert tree.root.right.right is not None and tree.root.right.right.value == 7


def test_all_four_traversals_match_expected_sequences() -> None:
    tree = build_assignment_binary_tree()
    pre = preorder_traversal(tree)
    ino = inorder_traversal(tree)
    post = postorder_traversal(tree)
    lvl = levelorder_traversal(tree)

    assert pre == EXPECTED_PREORDER
    assert ino == EXPECTED_INORDER
    assert post == EXPECTED_POSTORDER
    assert lvl == EXPECTED_LEVELORDER

    for seq in (pre, ino, post, lvl):
        assert len(seq) == 31
        assert sorted(seq) == list(range(1, 32))


def test_all_traversals_helper() -> None:
    tree = build_assignment_binary_tree()
    results = all_traversals(tree)
    assert set(results.keys()) == {"Pre-order", "In-order", "Post-order", "Level-order"}
    assert results["Pre-order"] == EXPECTED_PREORDER
    assert results["In-order"] == EXPECTED_INORDER
    assert results["Post-order"] == EXPECTED_POSTORDER
    assert results["Level-order"] == EXPECTED_LEVELORDER


def test_empty_binary_tree_handling() -> None:
    empty: BinaryTree[int] = BinaryTree()
    assert empty.is_empty() is True
    assert empty.node_count() == 0
    assert preorder_traversal(empty) == []
    assert inorder_traversal(empty) == []
    assert postorder_traversal(empty) == []
    assert levelorder_traversal(empty) == []
