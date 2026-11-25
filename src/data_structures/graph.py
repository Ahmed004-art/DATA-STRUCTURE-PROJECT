"""Reusable weighted, undirected Graph data structure."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from src.utils.validators import ValidationError


@dataclass(frozen=True)
class GraphEdge:
    """Represents an undirected weighted edge between two vertices."""

    u: str
    v: str
    weight: int | float


class WeightedGraph:
    """Weighted, undirected graph backed by an adjacency list.

    Supports vertex/edge addition with strict validation, duplicate-edge prevention,
    adjacency matrix generation, and BFS connectivity checks.
    """

    def __init__(self, name: str = "WeightedGraph") -> None:
        self.name = name
        self._vertices: list[str] = []
        self._adj: dict[str, dict[str, int | float]] = {}
        self._edges: list[GraphEdge] = []

    def add_vertex(self, vertex: str) -> None:
        """Add a vertex to the graph if not already present."""
        if not isinstance(vertex, str) or not vertex.strip():
            raise ValidationError("Vertex name must be a non-empty string.")
        v = vertex.strip()
        if v not in self._adj:
            self._vertices.append(v)
            self._adj[v] = {}

    def add_edge(self, u: str, v: str, weight: int | float) -> None:
        """Add an undirected weighted edge between existing vertices u and v.

        Rejects invalid/unknown vertices, self-loops, non-numeric or negative weights,
        and duplicate edges.
        """
        if u not in self._adj:
            raise ValidationError(f"Unknown vertex '{u}' in graph '{self.name}'.")
        if v not in self._adj:
            raise ValidationError(f"Unknown vertex '{v}' in graph '{self.name}'.")
        if u == v:
            raise ValidationError(f"Self-loops are not permitted ('{u}' -> '{v}').")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValidationError(f"Edge weight must be numeric, got {weight!r}.")
        if weight < 0:
            raise ValidationError(f"Edge weight cannot be negative, got {weight}.")
        if v in self._adj[u]:
            raise ValidationError(f"Duplicate edge between '{u}' and '{v}'.")

        self._adj[u][v] = weight
        self._adj[v][u] = weight
        self._edges.append(GraphEdge(u=u, v=v, weight=weight))

    def vertices(self) -> list[str]:
        """Return vertices in insertion order."""
        return list(self._vertices)

    def vertex_count(self) -> int:
        """Return number of vertices |V|."""
        return len(self._vertices)

    def edges(self) -> list[GraphEdge]:
        """Return all undirected edges in insertion order."""
        return list(self._edges)

    def edge_count(self) -> int:
        """Return number of undirected edges |E|."""
        return len(self._edges)

    def neighbors(self, vertex: str) -> dict[str, int | float]:
        """Return a copy of neighbor -> weight mapping for a vertex."""
        if vertex not in self._adj:
            raise ValidationError(f"Unknown vertex '{vertex}' in graph '{self.name}'.")
        return dict(self._adj[vertex])

    def has_edge(self, u: str, v: str) -> bool:
        """Return True if an undirected edge (u, v) exists."""
        return u in self._adj and v in self._adj[u]

    def get_weight(self, u: str, v: str) -> int | float:
        """Return the weight of edge (u, v)."""
        if not self.has_edge(u, v):
            raise ValidationError(f"No edge exists between '{u}' and '{v}'.")
        return self._adj[u][v]

    def adjacency_list(self) -> dict[str, list[tuple[str, int | float]]]:
        """Return sorted adjacency list representation."""
        return {
            v: sorted(self._adj[v].items(), key=lambda item: item[0])
            for v in self._vertices
        }

    def adjacency_matrix(self) -> tuple[list[str], list[list[int | float | None]]]:
        """Return (vertex_labels, matrix) where None denotes no direct edge."""
        labels = list(self._vertices)
        index = {v: i for i, v in enumerate(labels)}
        n = len(labels)
        matrix: list[list[int | float | None]] = [[None] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        for edge in self._edges:
            i, j = index[edge.u], index[edge.v]
            matrix[i][j] = edge.weight
            matrix[j][i] = edge.weight
        return labels, matrix

    def format_adjacency_matrix(self) -> str:
        """Return a formatted text table of the adjacency matrix ('-' for no edge)."""
        labels, matrix = self.adjacency_matrix()
        header = "    " + " ".join(f"{lbl:>3}" for lbl in labels)
        lines = [header, "    " + "-" * (4 * len(labels))]
        for lbl, row in zip(labels, matrix):
            cells = " ".join(f"{('-' if val is None else val):>3}" for val in row)
            lines.append(f"{lbl:>2} | {cells}")
        return "\n".join(lines)

    def is_connected(self) -> bool:
        """Check whether the graph is connected using BFS. O(|V| + |E|)."""
        if not self._vertices:
            return True
        visited: set[str] = {self._vertices[0]}
        queue: deque[str] = deque([self._vertices[0]])
        while queue:
            curr = queue.popleft()
            for nbr in self._adj[curr]:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)
        return len(visited) == len(self._vertices)

    def format_summary(self) -> str:
        """Return a readable summary of vertices, edge count, connectivity, and adjacency list."""
        lines = [
            f"Graph: {self.name}",
            f"Vertices ({self.vertex_count()}): {', '.join(self._vertices)}",
            f"Undirected Edges ({self.edge_count()}) | Connected: {self.is_connected()}",
            "Adjacency List:",
        ]
        for v, nbrs in self.adjacency_list().items():
            formatted = ", ".join(f"{nbr}({w})" for nbr, w in nbrs)
            lines.append(f"  {v}: [{formatted}]")
        return "\n".join(lines)
