# Milestone 2 — Stack & Tower of Hanoi Technical Notes

## 1. Stack Data Structure (`src/data_structures/stack.py`)

### Operations & Time/Space Complexity
| Operation | Description | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| `push(item)` | Append item to top of stack | $O(1)$ amortized | $O(1)$ per item |
| `pop()` | Remove and return top item (`StackUnderflowError` if empty) | $O(1)$ | $O(1)$ |
| `peek()` | Return top item without removal (`StackUnderflowError` if empty) | $O(1)$ | $O(1)$ |
| `is_empty()` | Return `True` if stack has no items | $O(1)$ | $O(1)$ |
| `size()` | Return current number of items | $O(1)$ | $O(1)$ |
| `display()` | Render stack items top-to-bottom | $O(n)$ | $O(n)$ |

Overall space complexity for $n$ stored elements is $O(n)$.

---

## 2. Tower of Hanoi (`src/algorithms/hanoi.py`)

### Recursive Formulation
To move $n$ disks from `Source` to `Destination` using `Auxiliary`:
1. Recursively move $n - 1$ disks from `Source` to `Auxiliary` (using `Destination`).
2. Move disk $n$ directly from `Source` to `Destination`.
3. Recursively move $n - 1$ disks from `Auxiliary` to `Destination` (using `Source`).

### Step-by-Step Example for $n = 3$ Disks ($2^3 - 1 = 7$ Moves)
1. Move disk 1 from `Source` -> `Destination`
2. Move disk 2 from `Source` -> `Auxiliary`
3. Move disk 1 from `Destination` -> `Auxiliary`
4. Move disk 3 from `Source` -> `Destination`
5. Move disk 1 from `Auxiliary` -> `Source`
6. Move disk 2 from `Auxiliary` -> `Destination`
7. Move disk 1 from `Source` -> `Destination`

### Complexity Analysis
- **Recurrence:** $T(n) = 2T(n - 1) + 1$, with $T(1) = 1$, giving $T(n) = 2^n - 1$.
- **Time Complexity:** $O(2^n)$.
- **Space Complexity:** $O(n)$ recursion call-stack depth; $O(2^n)$ if storing the full move list.
