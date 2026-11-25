"""Dijkstra's single-source shortest-path algorithm using a min-heap priority queue."""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass

from src.data_structures.graph import WeightedGraph
from src.utils.validators import ValidationError


@dataclass(frozen=True)
class DijkstraStep:
    """Records one vertex settlement step in Dijkstra's algorithm."""

    step: int
    vertex: str
    distance: float
    predecessor: str | None
    relaxed_neighbors: tuple[str, ...]


@dataclass(frozen=True)
class DijkstraResult:
    """Complete shortest-path results from a single source vertex."""

    graph_name: str
    source: str
    distances: dict[str, float]
    predecessors: dict[str, str | None]
    paths: dict[str, list[str]]
    steps: list[DijkstraStep]

    def path_to(self, target: str) -> tuple[float, list[str]]:
        """Return (distance, path) to target vertex."""
        if target not in self.distances:
            raise ValidationError(f"Unknown target vertex '{target}'.")
        return self.distances[target], self.paths[target]

    def tree_edges(self) -> list[tuple[str, str]]:
        """Return directed (predecessor, vertex) edges forming the shortest-path tree."""
        edges: list[tuple[str, str]] = []
        for vertex, pred in self.predecessors.items():
            if pred is not None:
                edges.append((pred, vertex))
        return edges

    def format_table(self) -> str:
        """Format shortest distances, predecessors, and paths as a readable table."""
        lines = [
            f"Dijkstra's Shortest Paths from '{self.source}' ({self.graph_name}):",
            f"{'Vertex':<8} {'Distance':<10} {'Pred':<8} {'Shortest Path'}",
            "-" * 58,
        ]
        for v, dist in self.distances.items():
            pred = self.predecessors[v] if self.predecessors[v] is not None else "-"
            if math.isinf(dist):
                dist_str = "INF"
                path_str = "Unreachable"
            else:
                dist_str = str(int(dist) if float(dist).is_integer() else dist)
                path_str = " -> ".join(self.paths[v])
            lines.append(f"{v:<8} {dist_str:<10} {pred:<8} {path_str}")
        return "\n".join(lines)


def _reconstruct_path(
    predecessors: dict[str, str | None], source: str, target: str, dist: float
) -> list[str]:
    """Reconstruct shortest path from source to target using predecessor links."""
    if math.isinf(dist):
        return []
    path: list[str] = []
    curr: str | None = target
    while curr is not None:
        path.append(curr)
        if curr == source:
            break
        curr = predecessors[curr]
    path.reverse()
    return path if path and path[0] == source else []


def dijkstra_shortest_paths(graph: WeightedGraph, source: str = "A") -> DijkstraResult:
    """Compute shortest paths from source to all vertices using Dijkstra's algorithm.

    Time Complexity:  O((|V| + |E|) log |V|) with a binary min-heap.
    Space Complexity: O(|V| + |E|) for distances, predecessors, and priority queue.
    """
    vertices = graph.vertices()
    if source not in vertices:
        raise ValidationError(f"Unknown source vertex '{source}' in '{graph.name}'.")

    for edge in graph.edges():
        if edge.weight < 0:
            raise ValidationError(
                f"Dijkstra's algorithm does not support negative edge weights "
                f"({edge.u}-{edge.v}: {edge.weight})."
            )

    distances: dict[str, float] = {v: math.inf for v in vertices}
    predecessors: dict[str, str | None] = {v: None for v in vertices}
    distances[source] = 0

    settled: set[str] = set()
    heap: list[tuple[float, str]] = [(0, source)]
    steps: list[DijkstraStep] = []

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)

        relaxed: list[str] = []
        for v, weight in sorted(graph.neighbors(u).items()):
            if v in settled:
                continue
            candidate = curr_dist + weight
            if candidate < distances[v]:
                distances[v] = candidate
                predecessors[v] = u
                heapq.heappush(heap, (candidate, v))
                relaxed.append(f"{v}={int(candidate) if float(candidate).is_integer() else candidate}")

        steps.append(
            DijkstraStep(
                step=len(steps) + 1,
                vertex=u,
                distance=curr_dist,
                predecessor=predecessors[u],
                relaxed_neighbors=tuple(relaxed),
            )
        )

    paths = {
        v: _reconstruct_path(predecessors, source, v, distances[v])
        for v in vertices
    }
    return DijkstraResult(
        graph_name=graph.name,
        source=source,
        distances=distances,
        predecessors=predecessors,
        paths=paths,
        steps=steps,
    )
