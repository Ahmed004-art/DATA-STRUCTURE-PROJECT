"""Exact Figure 2 weighted undirected graph from assignment PDF Page 3."""

from __future__ import annotations

from src.data_structures.graph import WeightedGraph

FIGURE_2_VERTICES: list[str] = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"
]

FIGURE_2_EDGES: list[tuple[str, str, int]] = [
    ("A", "B", 2),
    ("B", "C", 3),
    ("A", "D", 15),
    ("B", "D", 5),
    ("B", "E", 17),
    ("D", "E", 4),
    ("D", "G", 6),
    ("E", "G", 11),
    ("E", "C", 12),
    ("C", "F", 18),
    ("E", "F", 13),
    ("E", "H", 7),
    ("G", "H", 19),
    ("H", "F", 14),
    ("G", "I", 8),
    ("I", "J", 1),
    ("G", "J", 1),
    ("H", "J", 16),
    ("A", "I", 9),
]

# Approximate 2D layout matching Page 3 Figure 2 for clear diagram rendering
FIGURE_2_POSITIONS: dict[str, tuple[float, float]] = {
    "A": (1.0, 5.4),
    "B": (3.2, 5.4),
    "C": (5.6, 5.2),
    "D": (2.2, 3.6),
    "E": (4.0, 3.6),
    "F": (6.6, 3.5),
    "G": (3.7, 1.8),
    "H": (5.5, 1.8),
    "I": (2.5, 0.5),
    "J": (5.9, 0.4),
}


def build_figure2_graph() -> WeightedGraph:
    """Build and return the exact 10-vertex, 19-edge Figure 2 graph."""
    graph = WeightedGraph(name="Figure 2 (Assignment Page 3)")
    for vertex in FIGURE_2_VERTICES:
        graph.add_vertex(vertex)
    for u, v, weight in FIGURE_2_EDGES:
        graph.add_edge(u, v, weight)
    return graph
