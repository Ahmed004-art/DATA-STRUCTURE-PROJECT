"""Diagram generation utilities synced to actual data structure and algorithm outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from src.algorithms.hanoi import solve_tower_of_hanoi
from src.algorithms.huffman import HuffmanNode, HuffmanResult
from src.data_structures.binary_tree import BinaryTree, TreeNode
from src.data_structures.graph import WeightedGraph
from src.data_structures.stack import Stack


def generate_stack_diagram(output_path: str | Path) -> Path:
    """Generate a visual diagram of actual Stack LIFO operations (push, peek, pop)."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    stack: Stack[int] = Stack()
    snapshots: list[tuple[str, list[int]]] = [("Initial (Empty)", stack.to_list())]
    for val in (10, 20, 30):
        stack.push(val)
        snapshots.append((f"push({val})\npeek()={stack.peek()}", stack.to_list()))
    popped = stack.pop()
    snapshots.append((f"pop() -> {popped}\npeek()={stack.peek()}", stack.to_list()))

    fig, axes = plt.subplots(1, len(snapshots), figsize=(13, 4.2))
    fig.suptitle(
        "Stack (LIFO) Operations — Push, Peek, and Pop Trace",
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )

    colors = ["#4C78A8", "#54A24B", "#F58518"]
    for ax, (title, items) in zip(axes, snapshots):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        ax.set_title(title, fontsize=9.5, fontweight="bold", pad=8)

        # Draw U-shaped stack container
        ax.plot([2, 2, 8, 8], [4.8, 0.8, 0.8, 4.8], color="#333333", linewidth=2.2)

        for idx, val in enumerate(items):
            y = 0.95 + idx * 1.15
            rect = patches.FancyBboxPatch(
                (2.4, y),
                5.2,
                0.95,
                boxstyle="round,pad=0.05",
                facecolor=colors[idx % len(colors)],
                edgecolor="#1F2937",
                linewidth=1.2,
            )
            ax.add_patch(rect)
            ax.text(
                5.0,
                y + 0.47,
                str(val),
                ha="center",
                va="center",
                color="white",
                fontsize=11,
                fontweight="bold",
            )
            if idx == len(items) - 1:
                ax.annotate(
                    "TOP",
                    xy=(7.8, y + 0.47),
                    xytext=(8.6, y + 0.47),
                    fontsize=8.5,
                    fontweight="bold",
                    color="#B91C1C",
                    va="center",
                    arrowprops={"arrowstyle": "->", "color": "#B91C1C", "lw": 1.3},
                )

        if not items:
            ax.text(5.0, 2.5, "Empty", ha="center", va="center", color="#6B7280", fontsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def generate_hanoi_diagram(output_path: str | Path, disks: int = 3) -> Path:
    """Generate a step-by-step state diagram from solve_tower_of_hanoi(disks)."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    moves = solve_tower_of_hanoi(disks, source="A", auxiliary="B", destination="C")
    rods: dict[str, list[int]] = {
        "A": list(range(disks, 0, -1)),
        "B": [],
        "C": [],
    }
    states: list[tuple[str, dict[str, list[int]]]] = [
        ("Initial State", {k: list(v) for k, v in rods.items()})
    ]
    for move in moves:
        disk = rods[move.source].pop()
        rods[move.destination].append(disk)
        states.append(
            (
                f"Step {move.step}: Disk {move.disk} ({move.source}->{move.destination})",
                {k: list(v) for k, v in rods.items()},
            )
        )

    cols = 4
    rows = (len(states) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(14, 3.2 * rows))
    fig.suptitle(
        f"Tower of Hanoi ({disks} Disks, {len(moves)} Moves = 2^{disks} - 1)",
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )

    disk_colors = {1: "#E45756", 2: "#F58518", 3: "#4C78A8", 4: "#54A24B"}
    flat_axes = list(axes.flat) if hasattr(axes, "flat") else [axes]

    for idx, ax in enumerate(flat_axes):
        if idx >= len(states):
            ax.axis("off")
            continue

        title, state = states[idx]
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 5)
        ax.axis("off")
        ax.set_title(title, fontsize=9.5, fontweight="bold", pad=6)

        # Base platform
        ax.plot([0.8, 11.2], [0.7, 0.7], color="#1F2937", linewidth=3)
        rod_x = {"A": 2.5, "B": 6.0, "C": 9.5}
        for name, x in rod_x.items():
            ax.plot([x, x], [0.7, 3.9], color="#4B5563", linewidth=2.5, zorder=1)
            ax.text(x, 0.25, f"Rod {name}", ha="center", va="center", fontsize=8.5, fontweight="bold")
            for level, disk in enumerate(state[name]):
                width = 0.7 + disk * 0.55
                y = 0.75 + level * 0.65
                rect = patches.FancyBboxPatch(
                    (x - width / 2, y),
                    width,
                    0.52,
                    boxstyle="round,pad=0.03",
                    facecolor=disk_colors.get(disk, "#72B7B2"),
                    edgecolor="#111827",
                    linewidth=1.0,
                    zorder=2,
                )
                ax.add_patch(rect)
                ax.text(
                    x,
                    y + 0.26,
                    str(disk),
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=8.5,
                    fontweight="bold",
                    zorder=3,
                )

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def _compute_binary_tree_positions(root: TreeNode[int]) -> dict[int, tuple[float, float]]:
    """Compute (x, y) coordinates for each node using inorder x-spacing and depth y."""
    positions: dict[int, tuple[float, float]] = {}
    x_counter = 0

    def _assign(node: TreeNode[int] | None, depth: int) -> None:
        nonlocal x_counter
        if node is None:
            return
        _assign(node.left, depth + 1)
        positions[node.value] = (float(x_counter), float(-depth * 1.8))
        x_counter += 1
        _assign(node.right, depth + 1)

    _assign(root, 0)
    return positions


def _draw_tree_edges(
    ax: plt.Axes,
    node: TreeNode[int] | None,
    positions: dict[int, tuple[float, float]],
) -> None:
    """Recursively draw parent-child edges."""
    if node is None:
        return
    x0, y0 = positions[node.value]
    for child in (node.left, node.right):
        if child is not None:
            x1, y1 = positions[child.value]
            ax.plot([x0, x1], [y0, y1], color="#6B7280", linewidth=1.4, zorder=1)
            _draw_tree_edges(ax, child, positions)


def generate_binary_tree_diagram(
    tree: BinaryTree[int], output_path: str | Path
) -> Path:
    """Generate a clean diagram of the exact 31-node binary tree."""
    if tree.root is None:
        raise ValueError("Cannot draw an empty binary tree.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    positions = _compute_binary_tree_positions(tree.root)

    fig, ax = plt.subplots(figsize=(16, 7.2))
    _draw_tree_edges(ax, tree.root, positions)

    for val, (x, y) in positions.items():
        circle = patches.Circle(
            (x, y), radius=0.45, facecolor="#2563EB", edgecolor="#1E3A8A", linewidth=1.5, zorder=2
        )
        ax.add_patch(circle)
        ax.text(
            x,
            y,
            str(val),
            ha="center",
            va="center",
            color="white",
            fontsize=9.5,
            fontweight="bold",
            zorder=3,
        )

    ax.set_title(
        "Assignment Binary Tree (31 Nodes, Levels 0–4)",
        fontsize=14,
        fontweight="bold",
        pad=14,
    )
    ax.set_xlim(-1, 31)
    ax.set_ylim(-8.5, 1.2)
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def generate_graph_diagram(
    graph: WeightedGraph,
    positions: dict[str, tuple[float, float]],
    output_path: str | Path,
    title: str,
    highlighted_edges: set[tuple[str, str]] | None = None,
    highlight_color: str = "#DC2626",
    vertex_labels: dict[str, str] | None = None,
) -> Path:
    """Render a weighted undirected graph with optional highlighted edges and node labels."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized_highlights: set[tuple[str, str]] = set()
    if highlighted_edges:
        for u, v in highlighted_edges:
            normalized_highlights.add((u, v))
            normalized_highlights.add((v, u))

    fig, ax = plt.subplots(figsize=(10.5, 6.8))

    for edge in graph.edges():
        x0, y0 = positions[edge.u]
        x1, y1 = positions[edge.v]
        is_hl = (edge.u, edge.v) in normalized_highlights
        if highlighted_edges is None:
            color, lw, alpha, zorder = "#374151", 2.0, 0.9, 1
        elif is_hl:
            color, lw, alpha, zorder = highlight_color, 3.6, 1.0, 2
        else:
            color, lw, alpha, zorder = "#D1D5DB", 1.3, 0.7, 1

        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, alpha=alpha, zorder=zorder)

        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        label_color = "#111827" if (highlighted_edges is None or is_hl) else "#9CA3AF"
        ax.text(
            mx,
            my,
            str(edge.weight),
            ha="center",
            va="center",
            fontsize=9.2,
            fontweight="bold" if (highlighted_edges is None or is_hl) else "normal",
            color=label_color,
            bbox={
                "boxstyle": "round,pad=0.16",
                "facecolor": "white",
                "edgecolor": color if is_hl else "#E5E7EB",
                "alpha": 0.95,
            },
            zorder=3,
        )

    for v in graph.vertices():
        x, y = positions[v]
        circle = patches.Circle(
            (x, y),
            radius=0.34,
            facecolor="#1D4ED8",
            edgecolor="#1E3A8A",
            linewidth=1.8,
            zorder=4,
        )
        ax.add_patch(circle)
        ax.text(
            x,
            y,
            v,
            ha="center",
            va="center",
            color="white",
            fontsize=11,
            fontweight="bold",
            zorder=5,
        )
        if vertex_labels and v in vertex_labels:
            ax.text(
                x,
                y - 0.50,
                vertex_labels[v],
                ha="center",
                va="center",
                fontsize=8.2,
                fontweight="bold",
                color="#B91C1C",
                bbox={"boxstyle": "round,pad=0.12", "facecolor": "#FEF2F2", "edgecolor": "#FECACA"},
                zorder=6,
            )

    xs = [pos[0] for pos in positions.values()]
    ys = [pos[1] for pos in positions.values()]
    ax.set_xlim(min(xs) - 0.9, max(xs) + 0.9)
    ax.set_ylim(min(ys) - 0.9, max(ys) + 0.8)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def generate_traversal_diagram(
    tree: BinaryTree[int],
    traversal_name: str,
    sequence: list[int],
    output_path: str | Path,
) -> Path:
    """Generate a binary tree diagram annotated with visitation order (#1..#31)."""
    if tree.root is None:
        raise ValueError("Cannot draw an empty binary tree.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    positions = _compute_binary_tree_positions(tree.root)
    visit_order = {node_val: idx + 1 for idx, node_val in enumerate(sequence)}

    fig, ax = plt.subplots(figsize=(16, 8.2))
    _draw_tree_edges(ax, tree.root, positions)

    cmap = plt.get_cmap("viridis")
    total = max(len(sequence) - 1, 1)

    for val, (x, y) in positions.items():
        step_num = visit_order[val]
        rgba = cmap((step_num - 1) / total)
        circle = patches.Circle(
            (x, y), radius=0.46, facecolor=rgba, edgecolor="#111827", linewidth=1.4, zorder=2
        )
        ax.add_patch(circle)
        luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
        text_color = "#111827" if luminance > 0.62 else "white"
        ax.text(
            x,
            y,
            str(val),
            ha="center",
            va="center",
            color=text_color,
            fontsize=9,
            fontweight="bold",
            zorder=3,
        )
        ax.text(
            x,
            y - 0.68,
            f"#{step_num}",
            ha="center",
            va="center",
            color="#B91C1C",
            fontsize=7.8,
            fontweight="bold",
            zorder=4,
        )

    seq_str = ", ".join(map(str, sequence))
    ax.set_title(
        f"{traversal_name} Traversal — Visitation Order (#1 to #{len(sequence)})",
        fontsize=14,
        fontweight="bold",
        pad=14,
    )
    fig.text(
        0.5,
        0.02,
        f"Order: {seq_str}",
        ha="center",
        va="bottom",
        fontsize=9.5,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#F3F4F6", "edgecolor": "#D1D5DB"},
    )
    ax.set_xlim(-1, 31)
    ax.set_ylim(-8.9, 1.2)
    ax.axis("off")
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def generate_huffman_tree_diagram(
    result: HuffmanResult, output_path: str | Path
) -> Path:
    """Generate a Huffman tree diagram with 0/1 edge labels and final codes."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    positions: dict[int, tuple[float, float]] = {}
    x_counter = 0

    def _assign(node: HuffmanNode | None, depth: int) -> None:
        nonlocal x_counter
        if node is None:
            return
        _assign(node.left, depth + 1)
        positions[id(node)] = (float(x_counter * 2.2), float(-depth * 2.1))
        x_counter += 1
        _assign(node.right, depth + 1)

    _assign(result.root, 0)

    fig, ax = plt.subplots(figsize=(11, 7.2))

    def _draw(node: HuffmanNode | None) -> None:
        if node is None:
            return
        x0, y0 = positions[id(node)]
        for child, bit in ((node.left, "0"), (node.right, "1")):
            if child is not None:
                x1, y1 = positions[id(child)]
                ax.plot([x0, x1], [y0, y1], color="#4B5563", linewidth=1.8, zorder=1)
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                offset = -0.28 if bit == "0" else 0.28
                ax.text(
                    mx + offset,
                    my + 0.1,
                    bit,
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="#B91C1C",
                    bbox={"boxstyle": "circle,pad=0.18", "facecolor": "white", "edgecolor": "#D1D5DB"},
                    zorder=4,
                )
                _draw(child)

        if node.is_leaf():
            assert node.symbol is not None
            code = result.codes[node.symbol]
            box = patches.FancyBboxPatch(
                (x0 - 0.85, y0 - 0.45),
                1.7,
                0.9,
                boxstyle="round,pad=0.08",
                facecolor="#16A34A",
                edgecolor="#14532D",
                linewidth=1.6,
                zorder=2,
            )
            ax.add_patch(box)
            ax.text(
                x0,
                y0 + 0.12,
                f"'{node.symbol}' : {node.frequency}",
                ha="center",
                va="center",
                color="white",
                fontsize=10,
                fontweight="bold",
                zorder=3,
            )
            ax.text(
                x0,
                y0 - 0.22,
                f"code: {code}",
                ha="center",
                va="center",
                color="#ECFDF5",
                fontsize=8.5,
                fontweight="bold",
                zorder=3,
            )
        else:
            circle = patches.Circle(
                (x0, y0), radius=0.45, facecolor="#2563EB", edgecolor="#1E3A8A", linewidth=1.6, zorder=2
            )
            ax.add_patch(circle)
            ax.text(
                x0,
                y0,
                str(node.frequency),
                ha="center",
                va="center",
                color="white",
                fontsize=10.5,
                fontweight="bold",
                zorder=3,
            )

    _draw(result.root)

    xs = [pos[0] for pos in positions.values()]
    ys = [pos[1] for pos in positions.values()]
    ax.set_xlim(min(xs) - 1.6, max(xs) + 1.6)
    ax.set_ylim(min(ys) - 1.2, max(ys) + 1.1)
    ax.set_title(
        f"Huffman Coding Tree (Left=0, Right=1) — Weighted Length: {result.weighted_bit_length} bits",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def generate_graph_diagram(
    graph: WeightedGraph,
    positions: dict[str, tuple[float, float]],
    output_path: str | Path,
    title: str,
    highlighted_edges: set[tuple[str, str]] | None = None,
    highlight_color: str = "#DC2626",
    vertex_labels: dict[str, str] | None = None,
) -> Path:
    """Render a weighted undirected graph with optional highlighted edges and node labels."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized_highlights: set[tuple[str, str]] = set()
    if highlighted_edges:
        for u, v in highlighted_edges:
            normalized_highlights.add((u, v))
            normalized_highlights.add((v, u))

    fig, ax = plt.subplots(figsize=(10.5, 6.8))

    for edge in graph.edges():
        x0, y0 = positions[edge.u]
        x1, y1 = positions[edge.v]
        is_hl = (edge.u, edge.v) in normalized_highlights
        if highlighted_edges is None:
            color, lw, alpha, zorder = "#374151", 2.0, 0.9, 1
        elif is_hl:
            color, lw, alpha, zorder = highlight_color, 3.6, 1.0, 2
        else:
            color, lw, alpha, zorder = "#D1D5DB", 1.3, 0.7, 1

        ax.plot([x0, x1], [y0, y1], color=color, linewidth=lw, alpha=alpha, zorder=zorder)

        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        label_color = "#111827" if (highlighted_edges is None or is_hl) else "#9CA3AF"
        ax.text(
            mx,
            my,
            str(edge.weight),
            ha="center",
            va="center",
            fontsize=9.2,
            fontweight="bold" if (highlighted_edges is None or is_hl) else "normal",
            color=label_color,
            bbox={
                "boxstyle": "round,pad=0.16",
                "facecolor": "white",
                "edgecolor": color if is_hl else "#E5E7EB",
                "alpha": 0.95,
            },
            zorder=3,
        )

    for v in graph.vertices():
        x, y = positions[v]
        circle = patches.Circle(
            (x, y),
            radius=0.34,
            facecolor="#1D4ED8",
            edgecolor="#1E3A8A",
            linewidth=1.8,
            zorder=4,
        )
        ax.add_patch(circle)
        ax.text(
            x,
            y,
            v,
            ha="center",
            va="center",
            color="white",
            fontsize=11,
            fontweight="bold",
            zorder=5,
        )
        if vertex_labels and v in vertex_labels:
            ax.text(
                x,
                y - 0.50,
                vertex_labels[v],
                ha="center",
                va="center",
                fontsize=8.2,
                fontweight="bold",
                color="#B91C1C",
                bbox={"boxstyle": "round,pad=0.12", "facecolor": "#FEF2F2", "edgecolor": "#FECACA"},
                zorder=6,
            )

    xs = [pos[0] for pos in positions.values()]
    ys = [pos[1] for pos in positions.values()]
    ax.set_xlim(min(xs) - 0.9, max(xs) + 0.9)
    ax.set_ylim(min(ys) - 0.9, max(ys) + 0.8)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path
