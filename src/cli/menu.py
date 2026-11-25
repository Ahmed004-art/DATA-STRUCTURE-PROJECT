"""Interactive terminal CLI menu for DCOMP320 Data Structures & Algorithms."""

from __future__ import annotations

from typing import Callable

from src.algorithms.dijkstra import dijkstra_shortest_paths
from src.algorithms.hanoi import (
    LARGE_DISK_WARNING_THRESHOLD,
    expected_hanoi_moves,
    solve_tower_of_hanoi,
    verify_hanoi_moves,
)
from src.algorithms.huffman import (
    ASSIGNMENT_HUFFMAN_FREQUENCIES,
    decode_bits,
    encode_text,
    solve_huffman,
)
from src.algorithms.prim import prim_mst
from src.algorithms.traversals import (
    all_traversals,
    inorder_traversal,
    levelorder_traversal,
    postorder_traversal,
    preorder_traversal,
)
from src.data_structures.binary_tree import build_assignment_binary_tree
from src.data_structures.figure1_graph import build_figure1_graph
from src.data_structures.figure2_graph import build_figure2_graph
from src.data_structures.stack import (
    Stack,
    StackUnderflowError,
    is_balanced_parentheses,
    reverse_string_with_stack,
)
from src.utils.validators import ValidationError, parse_positive_int


def run_stack_demonstration() -> None:
    """Run a scripted demonstration of all Stack operations and practical uses."""
    print("\n=== Stack Data Structure Demonstration ===")
    stack: Stack[int] = Stack()
    print(f"Initial is_empty(): {stack.is_empty()}, size(): {stack.size()}")
    print(stack.display())

    for value in (10, 20, 30):
        stack.push(value)
        print(f"push({value}) -> size={stack.size()}, peek={stack.peek()}")

    print("\nCurrent stack state (top to bottom):")
    print(stack.display())

    print(f"pop() -> {stack.pop()} (new peek={stack.peek()}, size={stack.size()})")
    print(f"pop() -> {stack.pop()} (new peek={stack.peek()}, size={stack.size()})")
    print(f"pop() -> {stack.pop()} (is_empty={stack.is_empty()}, size={stack.size()})")

    print("\nTesting underflow handling on empty stack:")
    try:
        stack.pop()
    except StackUnderflowError as err:
        print(f"Caught expected error on pop(): {err}")

    try:
        stack.peek()
    except StackUnderflowError as err:
        print(f"Caught expected error on peek(): {err}")

    print("\nPractical Stack Applications:")
    sample_text = "DCOMP320"
    print(f"  String reversal: '{sample_text}' -> '{reverse_string_with_stack(sample_text)}'")
    for expr in ("{[()]}", "((1 + 2) * [3 - 4])", "([)]"):
        print(f"  Balanced brackets '{expr}': {is_balanced_parentheses(expr)}")


def run_interactive_stack(input_fn: Callable[[str], str] = input) -> None:
    """Interactive Stack playground allowing push, pop, peek, size, display."""
    stack: Stack[str] = Stack()
    while True:
        print("\n--- Interactive Stack Menu ---")
        print("1. Push item")
        print("2. Pop item")
        print("3. Peek top item")
        print("4. Check is_empty & size")
        print("5. Display stack")
        print("6. Run full Stack demonstration")
        print("0. Back to main menu")

        choice = input_fn("Select an option: ").strip()
        if choice == "0":
            return
        if choice == "1":
            item = input_fn("Enter value to push: ").strip()
            if not item:
                print("Error: Cannot push an empty value.")
                continue
            stack.push(item)
            print(f"Pushed '{item}'. Current size: {stack.size()}")
        elif choice == "2":
            try:
                popped = stack.pop()
                print(f"Popped: '{popped}'. Remaining size: {stack.size()}")
            except StackUnderflowError as err:
                print(f"Error: {err}")
        elif choice == "3":
            try:
                print(f"Top item (peek): '{stack.peek()}'")
            except StackUnderflowError as err:
                print(f"Error: {err}")
        elif choice == "4":
            print(f"is_empty(): {stack.is_empty()} | size(): {stack.size()}")
        elif choice == "5":
            print(stack.display())
        elif choice == "6":
            run_stack_demonstration()
        else:
            print("Invalid choice. Please enter 0-6.")


def run_hanoi_cli(
    input_fn: Callable[[str], str] = input,
    default_disks: int | None = None,
) -> None:
    """Run Tower of Hanoi solver with validation and large-disk confirmation."""
    print("\n=== Tower of Hanoi (Recursive Solver) ===")
    if default_disks is None:
        raw_n = input_fn("Enter number of disks (positive integer): ")
    else:
        raw_n = str(default_disks)
        print(f"Using n = {default_disks} disks.")

    try:
        n = parse_positive_int(raw_n, "number of disks")
    except ValidationError as err:
        print(f"Input Error: {err}")
        return

    expected = expected_hanoi_moves(n)
    if n > LARGE_DISK_WARNING_THRESHOLD and default_disks is None:
        confirm = input_fn(
            f"Warning: {n} disks require {expected:,} moves and will produce "
            f"extensive output. Continue? (y/n): "
        ).strip().lower()
        if confirm not in {"y", "yes"}:
            print("Operation cancelled.")
            return

    moves = solve_tower_of_hanoi(n)
    verify_hanoi_moves(n, moves)

    for move in moves:
        print(move.format_move())

    print(
        f"\nCompleted in {len(moves)} moves "
        f"(verified against 2^{n} - 1 = {expected})."
    )


def run_binary_tree_demonstration(mode: str = "all") -> None:
    """Display the 31-node assignment binary tree and requested traversal(s)."""
    tree = build_assignment_binary_tree()
    print("\n=== Assignment 31-Node Binary Tree & Traversals ===")
    assert tree.root is not None
    print(f"Root: {tree.root.value} | Total nodes: {tree.node_count()}")

    if mode == "preorder":
        seq = preorder_traversal(tree)
        print(f"Pre-order (Root -> Left -> Right) [{len(seq)} nodes]:")
        print(", ".join(map(str, seq)))
    elif mode == "inorder":
        seq = inorder_traversal(tree)
        print(f"In-order (Left -> Root -> Right) [{len(seq)} nodes]:")
        print(", ".join(map(str, seq)))
    elif mode == "postorder":
        seq = postorder_traversal(tree)
        print(f"Post-order (Left -> Right -> Root) [{len(seq)} nodes]:")
        print(", ".join(map(str, seq)))
    elif mode == "levelorder":
        seq = levelorder_traversal(tree)
        print(f"Level-order (BFS Queue) [{len(seq)} nodes]:")
        print(", ".join(map(str, seq)))
    else:
        for name, seq in all_traversals(tree).items():
            print(f"\n{name} ({len(seq)} nodes):")
            print("  " + ", ".join(map(str, seq)))


def run_binary_tree_menu(input_fn: Callable[[str], str] = input) -> None:
    """Interactive menu for Binary Tree and individual/all traversals."""
    while True:
        print("\n--- Binary Tree (31 Nodes) & Traversals ---")
        print("1. Pre-order traversal (Root -> Left -> Right)")
        print("2. In-order traversal (Left -> Root -> Right)")
        print("3. Post-order traversal (Left -> Right -> Root)")
        print("4. Level-order traversal (Queue / BFS)")
        print("5. Display all four traversals together")
        print("0. Back to main menu")

        choice = input_fn("Select an option: ").strip()
        if choice == "0":
            return
        mapping = {
            "1": "preorder",
            "2": "inorder",
            "3": "postorder",
            "4": "levelorder",
            "5": "all",
        }
        if choice in mapping:
            run_binary_tree_demonstration(mapping[choice])
        else:
            print("Invalid choice. Please enter 0-5.")


def run_huffman_demonstration(
    input_fn: Callable[[str], str] = input,
    interactive: bool = False,
) -> None:
    """Run Huffman coding on the exact assignment frequencies and optionally encode text."""
    print("\n=== Huffman Coding Demonstration ===")
    print("Input Frequencies:", ASSIGNMENT_HUFFMAN_FREQUENCIES)
    result = solve_huffman(ASSIGNMENT_HUFFMAN_FREQUENCIES)

    print("\nMerge Sequence (Priority Queue):")
    for step in result.merge_steps:
        print(
            f"  Step {step.step}: {step.left_label} ({step.left_freq}) + "
            f"{step.right_label} ({step.right_freq}) -> "
            f"{step.merged_label} ({step.merged_freq})"
        )

    print("\nFinal Huffman Codes (Left=0, Right=1):")
    for sym, freq in result.frequencies.items():
        code = result.codes[sym]
        print(f"  Symbol '{sym}' | Freq: {freq:>2} | Code: {code:<4} | Bits: {len(code)}")

    sample_message = "abcde"
    encoded_sample = encode_text(sample_message, result.codes)
    decoded_sample = decode_bits(encoded_sample, result.root)
    print(f"\nEncoded '{sample_message}': {encoded_sample} ({len(encoded_sample)} bits)")
    print(f"Decoded verification: '{decoded_sample}'")
    print(f"Weighted Encoded File Length (sum freq * len): {result.weighted_bit_length} bits")

    if interactive:
        custom = input_fn(
            "\nEnter a custom string using {a, b, c, d, e} to encode (or press Enter to skip): "
        ).strip()
        if custom:
            try:
                bits = encode_text(custom, result.codes)
                decoded = decode_bits(bits, result.root)
                print(f"Encoded '{custom}': {bits} ({len(bits)} bits)")
                print(f"Decoded check: '{decoded}'")
            except ValidationError as err:
                print(f"Input Error: {err}")


def run_graph_demonstration(mode: str = "all") -> None:
    """Run requested graph views, adjacency matrices, Dijkstra, and Prim algorithms."""
    fig1 = build_figure1_graph()
    fig2 = build_figure2_graph()

    if mode in {"fig1_info", "all"}:
        print("\n" + fig1.format_summary())
    if mode in {"fig2_info", "all"}:
        print("\n" + fig2.format_summary())
    if mode in {"matrices", "all"}:
        print("\n=== Figure 1 Adjacency Matrix ===")
        print(fig1.format_adjacency_matrix())
        print("\n=== Figure 2 Adjacency Matrix ===")
        print(fig2.format_adjacency_matrix())
    if mode in {"fig1_dijkstra", "all"}:
        res1 = dijkstra_shortest_paths(fig1, "A")
        print("\n" + res1.format_table())
    if mode in {"fig1_a_to_l", "all"}:
        res1 = dijkstra_shortest_paths(fig1, "A")
        cost, path = res1.path_to("L")
        cost_int = int(cost) if float(cost).is_integer() else cost
        print(f"\nFigure 1 Shortest Path A -> L: {' -> '.join(path)} (Total Cost: {cost_int})")
    if mode in {"fig2_dijkstra", "all"}:
        res2 = dijkstra_shortest_paths(fig2, "A")
        print("\n" + res2.format_table())
    if mode in {"fig1_prim", "all"}:
        mst1 = prim_mst(fig1, "A")
        print("\n" + mst1.format_summary())
    if mode in {"fig2_prim", "all"}:
        mst2 = prim_mst(fig2, "A")
        print("\n" + mst2.format_summary())


def run_graph_menu(input_fn: Callable[[str], str] = input) -> None:
    """Interactive menu for Figure 1 & Figure 2 Graph Algorithms."""
    while True:
        print("\n--- Graph Algorithms (Figure 1 & Figure 2) ---")
        print("1. View Figure 1 (Vertices, Edges & Adjacency List)")
        print("2. View Figure 2 (Vertices, Edges & Adjacency List)")
        print("3. Display Adjacency Matrices (Figure 1 & Figure 2)")
        print("4. Run Dijkstra on Figure 1 (from A to all vertices)")
        print("5. Run Dijkstra on Figure 2 (from A to all vertices)")
        print("6. Run Prim's MST on Figure 1")
        print("7. Run Prim's MST on Figure 2")
        print("8. View Figure 1 Shortest Path A -> L")
        print("9. Run all Graph demonstrations")
        print("0. Back to main menu")

        choice = input_fn("Select an option: ").strip()
        if choice == "0":
            return
        mapping = {
            "1": "fig1_info",
            "2": "fig2_info",
            "3": "matrices",
            "4": "fig1_dijkstra",
            "5": "fig2_dijkstra",
            "6": "fig1_prim",
            "7": "fig2_prim",
            "8": "fig1_a_to_l",
            "9": "all",
        }
        if choice in mapping:
            run_graph_demonstration(mapping[choice])
        else:
            print("Invalid choice. Please enter 0-9.")


def main_menu(input_fn: Callable[[str], str] = input) -> None:
    """Run the main interactive terminal menu."""
    while True:
        print("\n==============================================")
        print(" DCOMP320 — Data Structures & Algorithms CLI")
        print("==============================================")
        print("1. Stack Operations & Demonstrations")
        print("2. Tower of Hanoi (Recursive)")
        print("3. Binary Tree (31 Nodes) & Traversals")
        print("4. Huffman Coding (a, b, c, d, e)")
        print("5. Graph Algorithms (Dijkstra & Prim)")
        print("0. Exit")

        choice = input_fn("Choose an option: ").strip()
        if choice == "0":
            print("Exiting DCOMP320 CLI. Goodbye!")
            return
        if choice == "1":
            run_interactive_stack(input_fn=input_fn)
        elif choice == "2":
            run_hanoi_cli(input_fn=input_fn)
        elif choice == "3":
            run_binary_tree_menu(input_fn=input_fn)
        elif choice == "4":
            run_huffman_demonstration(input_fn=input_fn, interactive=True)
        elif choice == "5":
            run_graph_menu(input_fn=input_fn)
        else:
            print("Invalid selection. Please choose a valid menu option.")
