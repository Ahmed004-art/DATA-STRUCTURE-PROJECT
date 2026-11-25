# Milestone 4 — Graph Algorithms (Dijkstra & Prim) Technical Notes

## 1. Graph Theory & Representation

A **weighted undirected graph** $G = (V, E, w)$ consists of a set of vertices $V$, a set of unordered vertex pairs (edges) $E \subseteq \{\{u, v\} : u, v \in V, u \neq v\}$, and a weight function $w: E \to \mathbb{R}_{\ge 0}$.

Our implementation (`src/data_structures/graph.py`) maintains:
- An **adjacency list** (`dict[str, dict[str, int | float]]`) for $O(1)$ edge lookup and efficient $O(\deg(u))$ neighbor iteration in priority-queue algorithms.
- An **adjacency matrix** (`|V| × |V|` symmetric table) generated on demand for clear tabular reporting.

---

## 2. Supplied Graphs & Adjacency Matrices

### Figure 1 (12 Vertices `A–L`, 19 Undirected Edges)
```text
      A   B   C   D   E   F   G   H   I   J   K   L
    ------------------------------------------------
 A |  0   -   -   4   -   -   -   -   -   -   -   -
 B |  -   0   2   8   -   -   -   -   -   -   -   -
 C |  -   2   0   -   5   -   -   -   -  10   -   -
 D |  4   8   -   0   -   6   3   9   -   -   6   -
 E |  -   -   5   -   0   -   -   4   9   2   -   -
 F |  -   -   -   6   -   0   1   -   -   -   7   -
 G |  -   -   -   3   -   1   0   -   -   -   4   -
 H |  -   -   -   9   4   -   -   0   3   -   6   -
 I |  -   -   -   -   9   -   -   3   0   7   -   -
 J |  -   -  10   -   2   -   -   -   7   0   -   1
 K |  -   -   -   6   -   7   4   6   -   -   0   -
 L |  -   -   -   -   -   -   -   -   -   1   -   0
```

### Figure 2 (10 Vertices `A–J`, 19 Undirected Edges)
```text
      A   B   C   D   E   F   G   H   I   J
    ----------------------------------------
 A |  0   2   -  15   -   -   -   -   9   -
 B |  2   0   3   5  17   -   -   -   -   -
 C |  -   3   0   -  12  18   -   -   -   -
 D | 15   5   -   0   4   -   6   -   -   -
 E |  -  17  12   4   0  13  11   7   -   -
 F |  -   -  18   -  13   0   -  14   -   -
 G |  -   -   -   6  11   -   0  19   8   1
 H |  -   -   -   -   7  14  19   0   -  16
 I |  9   -   -   -   -   -   8   -   0   1
 J |  -   -   -   -   -   -   1  16   1   0
```

---

## 3. Dijkstra's Shortest-Path Algorithm (`src/algorithms/dijkstra.py`)

Dijkstra's algorithm greedily settles the unvisited vertex $u$ with the smallest tentative distance $d[u]$ from source $A$, relaxing each outgoing edge $(u, v)$ whenever $d[u] + w(u, v) < d[v]$.

### Figure 1 Results (Source: `A`)
- **Shortest Path `A -> L`:** `A -> D -> H -> E -> J -> L` (**Total Cost = 20**)
- **All Shortest Paths:**
  - `A`: `0` (`A`)
  - `B`: `12` (`A -> D -> B`)
  - `C`: `14` (`A -> D -> B -> C`)
  - `D`: `4` (`A -> D`)
  - `E`: `17` (`A -> D -> H -> E`)
  - `F`: `8` (`A -> D -> G -> F`)
  - `G`: `7` (`A -> D -> G`)
  - `H`: `13` (`A -> D -> H`)
  - `I`: `16` (`A -> D -> H -> I`)
  - `J`: `19` (`A -> D -> H -> E -> J`)
  - `K`: `10` (`A -> D -> K`)
  - `L`: `20` (`A -> D -> H -> E -> J -> L`)

### Figure 2 Results (Source: `A`)
- `A`: `0` (`A`)
- `B`: `2` (`A -> B`)
- `C`: `5` (`A -> B -> C`)
- `D`: `7` (`A -> B -> D`)
- `E`: `11` (`A -> B -> D -> E`)
- `F`: `23` (`A -> B -> C -> F`)
- `G`: `11` (`A -> I -> J -> G`)
- `H`: `18` (`A -> B -> D -> E -> H`)
- `I`: `9` (`A -> I`)
- `J`: `10` (`A -> I -> J`)

---

## 4. Prim's Minimum Spanning Tree (`src/algorithms/prim.py`)

Starting from vertex `A`, Prim's algorithm repeatedly selects the minimum-weight edge crossing the cut between visited and unvisited vertices until all $|V|$ vertices are connected using $|V| - 1$ edges.

- **Figure 1 MST (11 edges, Total Weight = 35):**
  `A-D (4)`, `D-G (3)`, `G-F (1)`, `G-K (4)`, `K-H (6)`, `H-I (3)`, `H-E (4)`, `E-J (2)`, `J-L (1)`, `E-C (5)`, `C-B (2)`.
- **Figure 2 MST (9 edges, Total Weight = 42):**
  `A-B (2)`, `B-C (3)`, `B-D (5)`, `D-E (4)`, `D-G (6)`, `G-J (1)`, `J-I (1)`, `E-H (7)`, `E-F (13)`.

---

## 5. Complexity & Comparison: Dijkstra vs. Prim

| Aspect | Dijkstra's Algorithm | Prim's Algorithm |
| :--- | :--- | :--- |
| **Problem Solved** | Single-Source Shortest Paths | Minimum Spanning Tree (MST) |
| **Priority Queue Key** | Cumulative distance from source $A$: $d[u] + w(u, v)$ | Individual edge weight crossing the cut: $w(u, v)$ |
| **Edge Count in Result** | $|V| - 1$ edges in shortest-path tree (reachable vertices) | Exactly $|V| - 1$ edges for any connected graph |
| **Time Complexity (Min-Heap)** | $O((|V| + |E|) \log |V|)$ | $O((|V| + |E|) \log |V|)$ |
| **Space Complexity** | $O(|V| + |E|)$ | $O(|V| + |E|)$ |

*(Note: Both algorithms were independently verified in `tests/test_graph.py` against Bellman-Ford for shortest paths and Kruskal's Union-Find algorithm for MST weights.)*
