"""Prim's Minimum Spanning Tree (MST) algorithm using a min-heap priority queue."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from src.data_structures.graph import WeightedGraph
from src.utils.validators import ValidationError


@dataclass(frozen=True)
class PrimEdge:
    """Represents a single edge selected into Prim's Minimum Spanning Tree."""

    step: int
    u: str
    v: str
    weight: int | float
    reason: str


@dataclass(frozen=True)
class PrimResult:
    """Complete Minimum Spanning Tree result from Prim's algorithm."""

    graph_name: str
    start: str
    edges: list[PrimEdge]
    total_weight: int | float
    visited_vertices: list[str]
    is_spanning_tree: bool

    def format_summary(self) -> str:
        """Format selected MST edges, reasons, and total weight."""
        lines = [
            f"Prim's Minimum Spanning Tree from '{self.start}' ({self.graph_name}):",
            f"Selected Edges ({len(self.edges)}):",
        ]
        for e in self.edges:
            lines.append(
                f"  Step {e.step:>2}: {e.u} - {e.v} (weight={e.weight}) | {e.reason}"
            )
        lines.append(
            f"Total MST Weight: {self.total_weight} | "
            f"Vertices Connected: {len(self.visited_vertices)} | "
            f"Valid Spanning Tree: {self.is_spanning_tree}"
        )
        return "\n".join(lines)


def prim_mst(graph: WeightedGraph, start: str = "A") -> PrimResult:
    """Compute a Minimum Spanning Tree starting at `start` using Prim's algorithm.

    Time Complexity:  O((|V| + |E|) log |V|) with a binary min-heap.
    Space Complexity: O(|V| + |E|) for the priority queue and visited set.
    """
    vertices = graph.vertices()
    if start not in vertices:
        raise ValidationError(f"Unknown start vertex '{start}' in '{graph.name}'.")

    visited: set[str] = {start}
    visited_order: list[str] = [start]
    heap: list[tuple[int | float, str, str]] = []

    for nbr, weight in sorted(graph.neighbors(start).items()):
        heapq.heappush(heap, (weight, start, nbr))

    selected: list[PrimEdge] = []
    total_weight: int | float = 0

    while heap and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(heap)
        if v in visited:
            continue

        visited.add(v)
        visited_order.append(v)
        total_weight += weight
        selected.append(
            PrimEdge(
                step=len(selected) + 1,
                u=u,
                v=v,
                weight=weight,
                reason=f"Minimum-weight cut edge connecting visited '{u}' to unvisited '{v}'",
            )
        )

        for nbr, nbr_weight in sorted(graph.neighbors(v).items()):
            if nbr not in visited:
                heapq.heappush(heap, (nbr_weight, v, nbr))

    is_complete = len(visited) == len(vertices) and len(selected) == max(len(vertices) - 1, 0)
    return PrimResult(
        graph_name=graph.name,
        start=start,
        edges=selected,
        total_weight=total_weight,
        visited_vertices=visited_order,
        is_spanning_tree=is_complete,
    )
