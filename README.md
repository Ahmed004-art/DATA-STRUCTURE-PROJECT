# DCOMP320 — Data Structures and Algorithms Final Project

**Limkokwing University of Creative Technology (Sierra Leone)**  
Department of Information and Communication Technology  
Module: `DCOMP320` — Data Structures and Algorithm  

## Features Implemented (Through Milestone 4)

1. **Stack (`src/data_structures/stack.py`)**
   - Full LIFO implementation (`push`, `pop`, `peek`, `is_empty`, `size`, `display`), `StackUnderflowError`, and practical applications.
2. **Tower of Hanoi (`src/algorithms/hanoi.py`)**
   - Recursive solver with $2^n - 1$ verification, input validation, and large-disk warning (`n > 10`).
3. **Binary Tree & Four Traversals (`src/data_structures/binary_tree.py`, `src/algorithms/traversals.py`)**
   - Exact 31-node complete binary tree (`1..31`) with Pre-order, In-order, Post-order, and Level-order traversals.
4. **Huffman Coding (`src/algorithms/huffman.py`)**
   - Priority-queue (`heapq`) Huffman coding for `{a: 2, b: 4, c: 8, d: 16, e: 16}` (`96 bits` weighted length, `"abcde"` = `14 bits`).
5. **Graph Algorithms (`src/data_structures/graph.py`, `src/algorithms/dijkstra.py`, `src/algorithms/prim.py`)**
   - Exact Figure 1 (12 vertices, 19 edges) and Figure 2 (10 vertices, 19 edges) weighted undirected graphs.
   - Adjacency lists & matrices, Dijkstra's shortest paths (including Figure 1 `A -> L` = `20`), and Prim's MST (Figure 1 = `35`, Figure 2 = `42`).
6. **Interactive CLI (`main.py`, `src/cli/menu.py`)**
   - Menu-driven terminal interface plus non-interactive `--demo` flags.

## Setup & Execution

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Interactive CLI
```powershell
python main.py
```

### Run Scripted Demos
```powershell
python main.py --demo m2 --disks 3
python main.py --demo m3
python main.py --demo m4
python main.py --demo all
```

### Run Automated Test Suite
```powershell
python -m pytest -v
```
