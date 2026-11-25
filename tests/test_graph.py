"""Automated tests and independent verification for Figure 1 & 2 Graph Algorithms."""

from __future__ import annotations

import math

import pytest

from src.algorithms.dijkstra import dijkstra_shortest_paths
from src.algorithms.prim import prim_mst
from src.data_structures.figure1_graph import (
    FIGURE_1_EDGES,
    FIGURE_1_VERTICES,
    build_figure1_graph,
)
from src.data_structures.figure2_graph import (
    FIGURE_2_EDGES,
    FIGURE_2_VERTICES,
    build_figure2_graph,
)
from src.data_structures.graph import WeightedGraph
from src.utils.validators import ValidationError


def _bellman_ford_verify(graph: WeightedGraph, source: str) -> dict[str, float]:
    """Independent Bellman-Ford shortest-path implementation for cross-checking."""
    dist: dict[str, float] = {v: math.inf for v in graph.vertices()}
    dist[source] = 0
    edges = graph.edges()
    for _ in range(graph.vertex_count() - 1):
        updated = False
        for e in edges:
            if dist[e.u] + e.weight < dist[e.v]:
                dist[e.v] = dist[e.u] + e.weight
                updated = True
            if dist[e.v] + e.weight < dist[e.u]:
                dist[e.u] = dist[e.v] + e.weight
                updated = True
        if not updated:
            break
    return dist


def _kruskal_mst_weight(graph: WeightedGraph) -> tuple[int | float, int]:
    """Independent Kruskal's MST implementation using Union-Find for cross-checking."""
    parent = {v: v for v in graph.vertices()}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total: int | float = 0
    edge_count = 0
    for edge in sorted(graph.edges(), key=lambda e: (e.weight, e.u, e.v)):
        ru, rv = find(edge.u), find(edge.v)
        if ru != rv:
            parent[ru] = rv
            total += edge.weight
            edge_count += 1
    return total, edge_count


def test_figure1_structure_and_matrix() -> None:
    fig1 = build_figure1_graph()
    assert fig1.vertex_count() == 12
    assert fig1.vertices() == FIGURE_1_VERTICES
    assert fig1.edge_count() == 19
    assert fig1.is_connected() is True
    assert fig1.has_edge("A", "D") and fig1.has_edge("D", "A")
    assert fig1.get_weight("A", "D") == 4
    assert fig1.get_weight("J", "L") == 1

    labels, matrix = fig1.adjacency_matrix()
    assert labels == FIGURE_1_VERTICES
    assert len(matrix) == 12
    for i in range(12):
        assert matrix[i][i] == 0
        for j in range(12):
            assert matrix[i][j] == matrix[j][i]

    adj = fig1.adjacency_list()
    assert len(adj) == 12
    assert ("D", 4) in adj["A"]


def test_figure2_structure_and_matrix() -> None:
    fig2 = build_figure2_graph()
    assert fig2.vertex_count() == 10
    assert fig2.vertices() == FIGURE_2_VERTICES
    assert fig2.edge_count() == 19
    assert fig2.is_connected() is True
    assert fig2.has_edge("A", "B") and fig2.has_edge("B", "A")
    assert fig2.get_weight("A", "B") == 2
    assert fig2.get_weight("G", "J") == 1

    labels, matrix = fig2.adjacency_matrix()
    assert labels == FIGURE_2_VERTICES
    assert len(matrix) == 10
    for i in range(10):
        assert matrix[i][i] == 0
        for j in range(10):
            assert matrix[i][j] == matrix[j][i]


def test_graph_validation_and_error_handling() -> None:
    g = WeightedGraph("Test")
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 5)

    with pytest.raises(ValidationError):
        g.add_edge("A", "Z", 3)
    with pytest.raises(ValidationError):
        g.add_edge("A", "A", 1)
    with pytest.raises(ValidationError):
        g.add_edge("A", "B", 5)
    with pytest.raises(ValidationError):
        g.add_edge("A", "B", -2)


def test_dijkstra_figure1_and_independent_bellman_ford() -> None:
    fig1 = build_figure1_graph()
    res = dijkstra_shortest_paths(fig1, "A")
    expected_bf = _bellman_ford_verify(fig1, "A")
    assert res.distances == expected_bf

    cost, path = res.path_to("L")
    assert cost == expected_bf["L"]
    assert path[0] == "A" and path[-1] == "L"
    assert sum(fig1.get_weight(path[i], path[i + 1]) for i in range(len(path) - 1)) == cost

    # Verify every reconstructed path sums to its reported distance
    for v, dist in res.distances.items():
        p = res.paths[v]
        assert p[0] == "A" and p[-1] == v
        path_sum = sum(fig1.get_weight(p[i], p[i + 1]) for i in range(len(p) - 1))
        assert path_sum == dist


def test_dijkstra_figure2_and_independent_bellman_ford() -> None:
    fig2 = build_figure2_graph()
    res = dijkstra_shortest_paths(fig2, "A")
    expected_bf = _bellman_ford_verify(fig2, "A")
    assert res.distances == expected_bf

    for v, dist in res.distances.items():
        p = res.paths[v]
        assert p[0] == "A" and p[-1] == v
        path_sum = sum(fig2.get_weight(p[i], p[i + 1]) for i in range(len(p) - 1))
        assert path_sum == dist


def test_dijkstra_unreachable_and_negative_edge_rejection() -> None:
    g = WeightedGraph("Disconnected")
    for v in ("A", "B", "Z"):
        g.add_vertex(v)
    g.add_edge("A", "B", 3)

    res = dijkstra_shortest_paths(g, "A")
    assert res.distances["B"] == 3
    assert math.isinf(res.distances["Z"])
    assert res.paths["Z"] == []

    # Bypass add_edge validation to test Dijkstra's own negative-weight guard
    g._adj["A"]["B"] = -1  # noqa: SLF001
    g._adj["B"]["A"] = -1  # noqa: SLF001
    g._edges[0] = type(g._edges[0])("A", "B", -1)  # noqa: SLF001
    with pytest.raises(ValidationError, match="negative edge weights"):
        dijkstra_shortest_paths(g, "A")


def _assert_valid_mst(graph: WeightedGraph, mst_result: object) -> None:
    from src.algorithms.prim import PrimResult

    assert isinstance(mst_result, PrimResult)
    assert mst_result.is_spanning_tree is True
    assert len(mst_result.edges) == graph.vertex_count() - 1
    assert set(mst_result.visited_vertices) == set(graph.vertices())

    # Verify every edge exists in original graph and forms no cycles via Union-Find
    parent = {v: v for v in graph.vertices()}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    weight_sum = 0
    for edge in mst_result.edges:
        assert graph.has_edge(edge.u, edge.v)
        assert graph.get_weight(edge.u, edge.v) == edge.weight
        ru, rv = find(edge.u), find(edge.v)
        assert ru != rv, f"Cycle detected at edge {edge.u}-{edge.v}"
        parent[ru] = rv
        weight_sum += edge.weight

    assert weight_sum == mst_result.total_weight


def test_prim_figure1_and_figure2_with_kruskal_verification() -> None:
    fig1 = build_figure1_graph()
    mst1 = prim_mst(fig1, "A")
    _assert_valid_mst(fig1, mst1)
    k_weight1, k_edges1 = _kruskal_mst_weight(fig1)
    assert mst1.total_weight == k_weight1
    assert len(mst1.edges) == k_edges1 == len(FIGURE_1_VERTICES) - 1
    assert len(FIGURE_1_EDGES) == 19

    fig2 = build_figure2_graph()
    mst2 = prim_mst(fig2, "A")
    _assert_valid_mst(fig2, mst2)
    k_weight2, k_edges2 = _kruskal_mst_weight(fig2)
    assert mst2.total_weight == k_weight2
    assert len(mst2.edges) == k_edges2 == len(FIGURE_2_VERTICES) - 1
    assert len(FIGURE_2_EDGES) == 19
