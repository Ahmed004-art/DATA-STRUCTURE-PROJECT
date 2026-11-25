# DCOMP320 Final Project — Requirements & Architecture Specification

## 1. Assignment Metadata (from PDF Pages 1 & 4)

- **Institution:** Limkokwing University of Creative Technology — Sierra Leone
- **Department:** Department of Information and Communication Technology
- **Module:** DCOMP320 — Data Structures and Algorithm (Semester 03&05, Sept 2026 – Feb 2027)
- **Examiner:** Amandus Benjamin Coker (`amandus.bcoker@limkokwing.edu.sl`)
- **Weighting:** Group Project, 30% of module mark (100 total marks)
  - Stack: 15 marks
  - Binary Trees: 20 marks
  - Graph: 20 marks
  - Recursion: 15 marks
  - Documentation and GitHub: 5 marks
  - Individual Presentation: 25 marks
- **Report Formatting:** Tahoma, 10 pt, 1.15 line spacing, Justified alignment.

---

## 2. Authoritative Problem Inputs (Extracted from PDF)

### 2.1 Stack (Assessment Criteria — 15 Marks)
- Operations: `push`, `pop`, `peek`, `is_empty`, `display`.
- Error handling: explicit underflow exception on `pop`/`peek` when empty.
- Demonstrations: interactive & scripted demonstrations (e.g., LIFO trace, balanced-parentheses or reversal demo).

### 2.2 Problem 1: Tower of Hanoi (Recursion — 15 Marks)
- Recursive algorithm accepting user-defined integer $n \ge 1$ (number of disks).
- Step-by-step move sequence from source peg (`A`) to destination peg (`C`) using auxiliary peg (`B`).
- Total moves verified against $2^n - 1$.

### 2.3 Problem 2: Binary Tree & Traversals (Binary Trees — 20 Marks)
- Exact 31-node complete binary tree from Page 2:
  - Root: `1`
  - Level 1: `2` (L of 1), `3` (R of 1)
  - Level 2: `4, 5` (children of 2); `6, 7` (children of 3)
  - Level 3: `8, 9` (4); `10, 11` (5); `12, 13` (6); `14, 15` (7)
  - Level 4: `16, 17` (8); `18, 19` (9); `20, 21` (10); `22, 23` (11); `24, 25` (12); `26, 27` (13); `28, 29` (14); `30, 31` (15)
- Traversals: Pre-order, In-order, Post-order, Level-order.

### 2.4 Problem 3: Huffman Coding (Page 2)
- Symbols and frequencies: `a: 2`, `b: 4`, `c: 8`, `d: 16`, `e: 16` (total frequency = 46).
- Construct Huffman tree, derive prefix-free binary codes, encode symbols, and compute weighted encoded length $\sum f_i \cdot |code_i|$.

### 2.5 Problem 4: Graph Algorithms (Graph — 20 Marks, Page 2–3)
Both graphs are undirected, weighted graphs.

**Figure 1 (12 vertices: A–L, 19 edges):**
- `A-D: 4`
- `B-C: 2`, `B-D: 8`
- `C-E: 5`, `C-J: 10`
- `D-F: 6`, `D-G: 3`, `D-H: 9`, `D-K: 6`
- `E-H: 4`, `E-I: 9`, `E-J: 2`
- `F-G: 1`, `F-K: 7`
- `G-K: 4`
- `H-I: 3`, `H-K: 6`
- `I-J: 7`
- `J-L: 1`

**Figure 2 (10 vertices: A–J, 19 edges):**
- `A-B: 2`, `A-D: 15`, `A-I: 9`
- `B-C: 3`, `B-D: 5`, `B-E: 17`
- `C-E: 12`, `C-F: 18`
- `D-E: 4`, `D-G: 6`
- `E-F: 13`, `E-G: 11`, `E-H: 7`
- `F-H: 14`
- `G-H: 19`, `G-I: 8`, `G-J: 1`
- `H-J: 16`
- `I-J: 1`

Required outputs:
- Adjacency matrices for both graphs.
- Dijkstra's shortest paths: specifically `A -> L` on Figure 1 (plus full table `A -> all` for completeness), and `A -> all` vertices on Figure 2.
- Prim's Minimum Spanning Tree (MST) from `A` on both Figure 1 and Figure 2, reporting MST edges and total weight.

---

## 3. Proposed Modular Architecture

| Module / Path | Responsibility | Milestone |
| :--- | :--- | :--- |
| `src/data_structures/stack.py` | `Stack`, `StackUnderflowError`, `push`, `pop`, `peek`, `is_empty`, `display` | M2 |
| `src/algorithms/hanoi.py` | Recursive `solve_hanoi`, move recording, step-by-step formatting | M2 |
| `src/data_structures/binary_tree.py` | `TreeNode`, `BinaryTree`, builder for exact 31-node PDF tree | M3 |
| `src/algorithms/traversals.py` | `preorder`, `inorder`, `postorder`, `levelorder` | M3 |
| `src/algorithms/huffman.py` | `HuffmanNode`, tree builder, code table, encoder, weighted length | M3 |
| `src/data_structures/graph.py` | `WeightedGraph`, adjacency matrix/list, Figure 1 & Figure 2 builders | M4 |
| `src/algorithms/dijkstra.py` | Dijkstra's shortest path algorithm + step-by-step trace + path reconstruction | M4 |
| `src/algorithms/prim.py` | Prim's MST algorithm + step-by-step trace + total weight | M4 |
| `src/utils/validators.py` | Input validation & custom exception types | M2–M5 |
| `src/utils/visualizer.py` | Matplotlib/Pillow diagram generation synced to actual code outputs | M5–M6 |
| `src/cli/menu.py` | Interactive terminal menu with safe input handling | M5 |
| `main.py` | Clean application entry point | M5 |
| `tests/test_*.py` | Automated unit & integration tests | M2–M5 |

---

## 4. Ambiguities & Technical Risks

1. **Dijkstra vs. Prim Wording (Page 2, Problem 4a):**
   - *Ambiguity:* The PDF states *"Use Dijkstra's and Prim's algorithms to find the shortest path from vertex A to all the other vertices for both of the figures"*. Mathematically, Dijkstra's algorithm solves single-source shortest paths, whereas Prim's algorithm computes a Minimum Spanning Tree (MST), not shortest paths.
   - *Resolution:* Implement both algorithms faithfully — Dijkstra for single-source shortest paths (including `A -> L` on Figure 1 and `A -> all` on both figures) and Prim for MST (starting from `A` on both figures) — and explain the distinction clearly in the report.
2. **Huffman Tie-Breaking & Bit Assignment:**
   - *Ambiguity:* In `2, 4, 8, 16, 16`, merging `((a+b)+c)` yields weight `14`, which is less than `16`, and then `14 + 16 = 30` vs `16`. Left=`0` / Right=`1` vs Left=`1` / Right=`0` and tie-breaking order can produce different valid prefix-free codes with the same optimal weighted length.
   - *Resolution:* Use deterministic tie-breaking (frequency, then symbol/insertion order) with Left=`0`, Right=`1`, and document the exact tree and weighted length (expected optimal weighted length = $2\times 4 + 4\times 4 + 8\times 3 + 16\times 2 + 16\times 2$ or $2\times 4 + 4\times 4 + 8\times 3 + \dots$ — to be computed and verified by the actual algorithm in Milestone 3).
3. **Huffman "Length of the Encoded File":**
   - *Ambiguity:* Could refer to total weighted bit length $\sum f_i \cdot |code_i|$ (representing a file where each symbol occurs $f_i$ times) or the encoded length of the 5-character string `"abcde"`.
   - *Resolution:* Compute and display both: the primary weighted encoded length for the frequency distribution and the bit length for the single-occurrence string `"abcde"`.
4. **Stack Problem Absence in Section 2:**
   - *Ambiguity:* Stack carries 15/100 marks in Assessment Criteria (Page 4) but has no numbered problem in Section 2.
   - *Resolution:* Provide a complete `Stack` class with all standard operations, underflow handling, and practical demonstrations in the CLI and report.
5. **Environment Dependencies:**
   - *Risk:* `python-docx` and `pillow` are currently installed, while `matplotlib` and `pytest` are not yet installed in the local Python 3.12 environment. We will install them (or verify `unittest` compatibility) when needed in Milestones 2–6.
