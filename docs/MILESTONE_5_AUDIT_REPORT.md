# Milestone 5 — Technical Audit & Verification Report

## 1. Project-Wide Inspection Findings
All repository files (`main.py`, `src/`, `tests/`, `diagrams/`, `docs/`, `README.md`, `requirements.txt`, `.gitignore`) were inspected:
- **Architecture & Imports:** Clean modular separation across `src/data_structures/`, `src/algorithms/`, `src/utils/`, and `src/cli/`. Absolute `src.*` imports work consistently without circular or broken imports.
- **Dependencies:** `requirements.txt` (`matplotlib`, `pillow`, `python-docx`, `pytest`) contains only required project dependencies (`python-docx` is reserved for Milestone 6 report generation).
- **Security & Hygiene:** No hardcoded credentials, tokens, or private data exist in any tracked or untracked workspace file. `.gitignore` excludes `__pycache__/`, `.venv/`, `.pytest_cache/`, `.env`, and IDE metadata.

---

## 2. Algorithm Correctness Results
- **Stack (`src/data_structures/stack.py`):** Verified strict LIFO behavior across `push`, `pop`, `peek`, `is_empty`, `size`, `display`, and `StackUnderflowError` on empty `pop()`/`peek()`.
- **Tower of Hanoi (`src/algorithms/hanoi.py`):** Verified genuine recursive sequence, $2^n - 1$ move count, rod-ordering legality (`verify_hanoi_moves`), and rejection of non-positive / non-integer inputs.
- **Binary Tree & Traversals (`src/data_structures/binary_tree.py`, `src/algorithms/traversals.py`):** Verified exact 31-node complete binary tree (`1..31`) and all four traversals (Pre-order, In-order, Post-order, Level-order) visiting every node once.
- **Huffman Coding (`src/algorithms/huffman.py`):** Verified priority-queue construction, deterministic prefix-free codes (`a: 1000`, `b: 1001`, `c: 101`, `d: 11`, `e: 0`), `"abcde"` = `14 bits`, weighted length = `96 bits`, and lossless decode roundtrip.
- **Dijkstra (`src/algorithms/dijkstra.py`):** Verified priority-queue relaxation, predecessor tracking, path reconstruction, unreachable handling, and negative-edge rejection.
- **Prim (`src/algorithms/prim.py`):** Verified priority-queue MST construction, `|V| - 1` edges, full connectivity, and exact total weights (`35` for Figure 1; `42` for Figure 2).

---

## 3. Graph Verification
- Both `figure1_graph.py` (12 vertices, 19 edges) and `figure2_graph.py` (10 vertices, 19 edges) were verified edge-by-edge against Page 3 of the assignment PDF.
- **Independent Cross-Checks (`tests/test_graph.py`):**
  - Bellman-Ford independently confirmed all Dijkstra distances on Figure 1 and Figure 2, including `A -> L = 20` (`A -> D -> H -> E -> J -> L`).
  - Kruskal's Union-Find MST independently confirmed Prim's total MST weights (`35` and `42`) and cycle-free connectivity.

---

## 4. Integration Testing
- Added `tests/test_cli.py` (6 integration tests) covering `--demo all`, main menu navigation, invalid menu selections, interactive Stack underflow/empty-push handling, Tower of Hanoi invalid input and `n > 10` cancellation, Binary Tree submenu, Huffman invalid-symbol handling, and Graph menu navigation.

---

## 5. Full Pytest Results
- Command: `python -m pytest -v`
- Result: **45 passed, 0 failed** in `0.30s` across `test_binary_tree.py` (4), `test_cli.py` (6), `test_graph.py` (7), `test_hanoi.py` (16), `test_huffman.py` (5), `test_stack.py` (7).

---

## 6. Clean Environment Results
- Created a fresh virtual environment (`%TEMP%\dcomp320_clean_venv`), installed dependencies solely from `requirements.txt`, ran `python -m pytest -v` (**45 passed**), ran `python main.py --demo all --disks 3` (**exit code 0**), and removed the temporary venv.

---

## 7. Diagram Inspection Results
All 15 generated PNG diagrams in `diagrams/` were visually inspected:
- `stack_operations.png`, `tower_of_hanoi_3_disks.png`
- `binary_tree_31_nodes.png`, `traversal_preorder.png`, `traversal_inorder.png`, `traversal_postorder.png`, `traversal_levelorder.png`, `huffman_tree.png`
- `figure1_graph.png`, `figure1_dijkstra_tree.png`, `figure1_dijkstra_a_to_l.png`, `figure1_prim_mst.png`
- `figure2_graph.png`, `figure2_dijkstra_tree.png`, `figure2_prim_mst.png`
All labels, weights, node badges, and highlighted paths are legible, non-clipped, and consistent with actual code outputs.

---

## 8. Bugs Identified & Corrected
- During initial creation of `tests/test_cli.py`, `test_hanoi_cli_invalid_and_large_disk_cancel` failed because the test's `_mock_inputs` helper discarded the prompt string instead of printing it to `stdout` like Python's `input(prompt)`. Updated `_mock_inputs` in `tests/test_cli.py` to print the prompt before returning the mocked response, after which all 45 tests passed.

---

## 9. Remaining Limitations
- `screenshots/` and the final Word report (`.docx`) are not yet created (scheduled for Milestone 6).
- `matplotlib` emits a harmless cache-directory fallback notice in restricted sandboxes when `AppData\Local\matplotlib` is not writable.

---

## 10. Final Technical Readiness Assessment
The codebase, automated test suite (45/45 passing), CLI integration, clean-environment installation, and all 15 diagrams are verified and ready for **Milestone 6** (Documentation, Genuine Screenshots, GitHub Push, and Submission ZIP).
