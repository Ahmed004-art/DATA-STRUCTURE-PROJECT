"""Exact Figure 1 weighted undirected graph from assignment PDF Page 3."""

from __future__ import annotations

from src.data_structures.graph import WeightedGraph

FIGURE_1_VERTICES: list[str] = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"
]

FIGURE_1_EDGES: list[tuple[str, str, int]] = [
    ("A", "D", 4),
    ("B", "D", 8),
    ("B", "C", 2),
    ("C", "E", 5),
    ("C", "J", 10),
    ("D", "F", 6),
    ("D", "G", 3),
    ("D", "H", 9),
    ("D", "K", 6),
    ("F", "G", 1),
    ("F", "K", 7),
    ("G", "K", 4),
    ("H", "K", 6),
    ("H", "E", 4),
    ("H", "I", 3),
    ("E", "I", 9),
    ("E", "J", 2),
    ("I", "J", 7),
    ("J", "L", 1),
]

# Approximate 2D layout matching Page 3 Figure 1 for clear diagram rendering
FIGURE_1_POSITIONS: dict[str, tuple[float, float]] = {
    "A": (1.6, 5.2),
    "B": (4.4, 5.2),
    "C": (7.2, 5.2),
    "D": (3.0, 3.8),
    "E": (5.6, 3.8),
    "F": (0.8, 2.3),
    "G": (2.1, 2.3),
    "H": (4.0, 2.3),
    "I": (5.6, 2.3),
    "J": (7.2, 2.3),
    "K": (3.0, 0.7),
    "L": (7.2, 0.7),
}


def build_figure1_graph() -> WeightedGraph:
    """Build and return the exact 12-vertex, 19-edge Figure 1 graph."""
    graph = WeightedGraph(name="Figure 1 (Assignment Page 3)")
    for vertex in FIGURE_1_VERTICES:
        graph.add_vertex(vertex)
    for u, v, weight in FIGURE_1_EDGES:
        graph.add_edge(u, v, weight)
    return graph
