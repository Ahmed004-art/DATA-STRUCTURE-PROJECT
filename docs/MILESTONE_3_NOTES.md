# Milestone 3 — Binary Tree, Traversals & Huffman Coding Technical Notes

## 1. Exact 31-Node Binary Tree (`src/data_structures/binary_tree.py`)

Reproduces the complete binary tree from Page 2 of the assignment PDF:
- **Root:** `1` (Level 0)
- **Level 1:** `2` (left of 1), `3` (right of 1)
- **Level 2:** `4, 5` (children of 2); `6, 7` (children of 3)
- **Level 3:** `8–15` (children of `4–7`)
- **Level 4 (Leaves):** `16–31` (children of `8–15`)

---

## 2. Four Tree Traversals (`src/algorithms/traversals.py`)

| Traversal | Order Rule | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Pre-order** | Root $\to$ Left $\to$ Right | $O(n)$ | $O(h) = O(\log n)$ balanced, $O(n)$ worst-case |
| **In-order** | Left $\to$ Root $\to$ Right | $O(n)$ | $O(h) = O(\log n)$ balanced, $O(n)$ worst-case |
| **Post-order** | Left $\to$ Right $\to$ Root | $O(n)$ | $O(h) = O(\log n)$ balanced, $O(n)$ worst-case |
| **Level-order** | Top-to-bottom, left-to-right via FIFO queue | $O(n)$ | $O(w) = O(n)$ (max width is $16$ leaves) |

### Actual Traversal Outputs (31 Nodes)
- **Pre-order:** `1, 2, 4, 8, 16, 17, 9, 18, 19, 5, 10, 20, 21, 11, 22, 23, 3, 6, 12, 24, 25, 13, 26, 27, 7, 14, 28, 29, 15, 30, 31`
- **In-order:** `16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 23, 1, 24, 12, 25, 6, 26, 13, 27, 3, 28, 14, 29, 7, 30, 15, 31`
- **Post-order:** `16, 17, 8, 18, 19, 9, 4, 20, 21, 10, 22, 23, 11, 5, 2, 24, 25, 12, 26, 27, 13, 6, 28, 29, 14, 30, 31, 15, 7, 3, 1`
- **Level-order:** `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31`

---

## 3. Huffman Coding (`src/algorithms/huffman.py`)

### Input Frequencies
`a: 2`, `b: 4`, `c: 8`, `d: 16`, `e: 16` (total frequency = 46).

### Priority Queue Merge Sequence (`heapq`, tie-break by `(frequency, order_id)`)
1. `a (2) + b (4) -> (a+b) (6)`
2. `(a+b) (6) + c (8) -> ((a+b)+c) (14)`
3. `((a+b)+c) (14) + d (16) -> (((a+b)+c)+d) (30)`
4. `e (16) + (((a+b)+c)+d) (30) -> (e+(((a+b)+c)+d)) (46)`

### Final Codes (Left = `0`, Right = `1`)
| Symbol | Frequency | Code | Code Length | Contribution ($f_i \times l_i$) |
| :---: | :---: | :---: | :---: | :---: |
| `a` | 2 | `1000` | 4 | 8 |
| `b` | 4 | `1001` | 4 | 16 |
| `c` | 8 | `101` | 3 | 24 |
| `d` | 16 | `11` | 2 | 32 |
| `e` | 16 | `0` | 1 | 16 |
| **Total** | **46** | — | **14 (`"abcde"`)** | **96 bits** |

### Why Huffman Coding Produces Variable-Length Prefix-Free Codes
Every input symbol is placed exclusively at a **leaf** of the binary tree, never at an internal node. Because no leaf is an ancestor of any other leaf, no codeword can ever be a prefix of another codeword (the prefix-free property). Consequently, encoded bitstreams can be decoded unambiguously left-to-right without delimiter bits, while assigning shorter codes to higher-frequency symbols (`e -> 0`, `d -> 11`) and longer codes to lower-frequency symbols (`a -> 1000`, `b -> 1001`).

### Complexity Analysis ($k$ distinct symbols, message length $m$)
- **Tree construction:** $O(k \log k)$ time using a binary min-heap; $O(k)$ space.
- **Code generation:** $O(k)$ time and $O(k)$ recursion stack space.
- **Encoding / Decoding:** $O(m)$ time where $m$ is the number of input symbols / output bits.

---

## 4. Investigation of Initial Milestone 2 Command Failure
During Milestone 2, the first test/diagram command failed immediately with `ParserError: The token '&&' is not a valid statement separator in this version`. The workspace shell is Windows PowerShell 5.1, which does not support Bash-style `&&` chaining. Switching to PowerShell's `; if ($?) { ... }` syntax resolved the issue completely, and all subsequent commands executed cleanly with exit code `0`.
