# 🧠 Python Data Structures

**CSC 341 — Data Structures & Algorithms | Assignment: Implementation of Core Data Structures**

This repository contains our group's implementation of four fundamental data structures as part of the CSC 341 assignment. Each file is fully annotated — comments explain the *why* behind every design decision, not just the *what*. Alongside the code, this README documents the standard algorithm (in plain steps) for every operation implemented, so the logic is clear independent of any language.

---

## 👥 Group Members

| Name | Structure Implemented |
|---|---|
| 243439 | Wonuola Yinyinloluwa Alonge
| 243472 | Olaniyan Oluwasemilore 
| 243467 | Obuwovo Victor
| 243480 | Oyeleke Raphae 
| 243424 | Abiodun Samuel Oluwatobi

---

## 📁 Repository Structure

```
python-data-structures/
├── linked_list.py        # Singly linked list — append, prepend, insert, delete, reverse
├── avl_tree.py           # Self-balancing BST — insert, delete, search, rotations
├── b_tree.py             # B-Tree — insert, search, split, traverse
├── graph.py              # Graph — BFS, DFS, Dijkstra, cycle detection, topological sort
└── README.md
```

---

## 📦 Implementations & Algorithms

---

### 🔗 Linked List (`linked_list.py`)

A singly linked list where each node holds a value and a pointer to the next node. There is no index-based access — every operation starts at the head and walks forward.

**Operations covered:**

| Method | Description | Time |
|---|---|---|
| `append(data)` | Add to the end | O(n) |
| `prepend(data)` | Add to the front | O(1) |
| `insert_after(target, data)` | Insert after a specific value | O(n) |
| `delete(data)` | Remove a node by value | O(n) |
| `search(data)` | Find a value and return its position | O(n) |
| `reverse()` | Flip the entire list in-place | O(n) |
| `length()` | Count all nodes | O(n) |
| `display()` | Print the chain | O(n) |

#### Algorithms

**Append**
```
1. Create a new node with the given data
2. If the list is empty, set head = new node and stop
3. Walk from head, following .next, until reaching a node where .next is None
4. Set that node's .next = new node
```

**Prepend**
```
1. Create a new node with the given data
2. Set new node's .next = current head
3. Set head = new node
```

**Insert After**
```
1. Start at head
2. Walk the list until finding the node whose data matches target
3. If found:
   a. Create a new node
   b. Set new node's .next = target node's .next
   c. Set target node's .next = new node
4. If target not found, report not found
```

**Delete**
```
1. If list is empty, stop
2. If head's data matches:
   a. Set head = head's .next and stop
3. Otherwise walk the list, tracking current and current.next
4. When current.next.data matches the target:
   a. Set current.next = current.next.next (skip over the target)
5. If end of list is reached without a match, report not found
```

**Search**
```
1. Start at head, set position counter = 0
2. At each node:
   a. If data matches, return position
   b. Otherwise advance to .next and increment position
3. If end of list is reached, report not found
```

**Reverse**
```
1. Initialise: previous = None, current = head
2. While current is not None:
   a. Save next = current.next
   b. Set current.next = previous    (point backwards)
   c. Set previous = current
   d. Set current = next
3. Set head = previous
```

**Quick example:**
```python
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.prepend(5)
ll.insert_after(10, 15)
ll.display()
# Output: 5 -> 10 -> 15 -> 20 -> None
```

---

### 🌳 AVL Tree (`avl_tree.py`)

A self-balancing Binary Search Tree. After every insert or delete, the tree checks its balance factor at each ancestor node and applies one of four rotations to maintain O(log n) height.

**Operations covered:**

| Method | Description | Time |
|---|---|---|
| `insert(data)` | Insert and auto-rebalance | O(log n) |
| `delete(data)` | Delete and auto-rebalance | O(log n) |
| `search(data)` | Returns True/False | O(log n) |
| `inorder()` | Print sorted output | O(n) |

#### Algorithms

**Insert**
```
1. Perform standard BST insert:
   a. If tree is empty, create root node
   b. If data < current node, recurse left
   c. If data > current node, recurse right
   d. If data == current node, ignore (no duplicates)
2. On the way back up the recursion stack:
   a. Update the height of the current node:
      height = 1 + max(left height, right height)
   b. Compute balance factor = left height - right height
   c. If balance > 1 and data < left child's data  → Right rotate (LL case)
   d. If balance < -1 and data > right child's data → Left rotate (RR case)
   e. If balance > 1 and data > left child's data   → Left rotate left child, then right rotate (LR case)
   f. If balance < -1 and data < right child's data → Right rotate right child, then left rotate (RL case)
```

**Right Rotation (fixes LL imbalance)**
```
Given unbalanced node z with left child y:
1. Set y's right child = z
2. Set z's left child = y's old right subtree (T3)
3. Update z's height first, then y's height
4. Return y as the new subtree root
```

**Left Rotation (fixes RR imbalance)**
```
Given unbalanced node z with right child y:
1. Set y's left child = z
2. Set z's right child = y's old left subtree (T2)
3. Update z's height first, then y's height
4. Return y as the new subtree root
```

**Delete**
```
1. Navigate to the target node using standard BST traversal
2. When found, handle one of three cases:
   a. No left child  → replace node with its right child
   b. No right child → replace node with its left child
   c. Two children   → find in-order successor (leftmost node of right subtree)
                       copy successor's data into current node
                       delete the successor from the right subtree
3. On the way back up the recursion stack:
   a. Update height
   b. Recompute balance factor
   c. Apply the same four rotation cases as insert
```

**Search**
```
1. Start at root
2. At each node:
   a. If data == node's data, return True
   b. If data < node's data, recurse left
   c. If data > node's data, recurse right
3. If a None node is reached, return False
```

**Four rotation cases:**

```
LL (Left-Left)   → rotate_right
RR (Right-Right) → rotate_left
LR (Left-Right)  → rotate_left on child, then rotate_right on root
RL (Right-Left)  → rotate_right on child, then rotate_left on root
```

**Quick example:**
```python
avl = AVLTree()
for val in [30, 20, 40, 10, 25, 35, 50]:
    avl.insert(val)
avl.inorder()
# Output: 10 -> 20 -> 25 -> 30 -> 35 -> 40 -> 50
avl.delete(20)
avl.inorder()
# Output: 10 -> 25 -> 30 -> 35 -> 40 -> 50
```

---

### 🌲 B-Tree (`b_tree.py`)

A multi-key self-balancing search tree designed for systems that read and write large blocks of data. Unlike a BST, each node holds multiple keys and can have multiple children. The tree grows only from the root, keeping all leaves at equal depth.

**Key property — minimum degree `t`:**
- Every non-root node has at least `t-1` keys and at most `2t-1` keys
- Every internal node has at least `t` children and at most `2t` children
- All leaves sit at the same depth

**Operations covered:**

| Method | Description | Time |
|---|---|---|
| `insert(key)` | Insert with proactive splitting | O(log n) |
| `search(key)` | Returns `(node, index)` or `None` | O(log n) |
| `traverse()` | In-order traversal | O(n) |

#### Algorithms

**Search**
```
1. Start at the root, set i = 0
2. At each node, advance i past all keys smaller than the target
3. If keys[i] == target, return (node, i)
4. If the node is a leaf, return None (not found)
5. Otherwise recurse into children[i]
```

**Insert**
```
1. If the root is full (has 2t-1 keys):
   a. Create a new empty root
   b. Make the old root a child of the new root
   c. Split the old root (see Split algorithm)
   d. Insert into the appropriate half of the new root
2. Otherwise call Insert-Non-Full on the root

Insert-Non-Full(node, key):
1. If node is a leaf:
   a. Shift all keys greater than key one position right
   b. Place key in the correct sorted position
2. If node is internal:
   a. Find the correct child index i for the key
   b. If children[i] is full:
      - Split children[i]
      - If key > promoted middle key, increment i
   c. Recurse into children[i]
```

**Split Child**
```
Given parent node and index of the full child:
1. Let full_child = parent.children[index]
2. Create new_child (same leaf status as full_child)
3. Set middle_key = full_child.keys[t-1]
4. Move full_child.keys[t:] into new_child.keys
5. Trim full_child.keys to full_child.keys[:t-1]
6. If not a leaf, move full_child.children[t:] into new_child.children
7. Insert new_child into parent.children at index+1
8. Insert middle_key into parent.keys at index
```

**Traverse (In-Order)**
```
1. For i from 0 to len(node.keys)-1:
   a. If not a leaf, recursively traverse children[i]
   b. Visit (print) keys[i]
2. If not a leaf, recursively traverse the last child children[len(keys)]
```

**Quick example:**
```python
btree = BTree(t=3)
for val in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(val)
btree.traverse()
# Output: 5 6 7 10 12 17 20 30
print(btree.search(12))  # (<BTreeNode>, 0)
print(btree.search(99))  # None
```

---

### 🕸️ Graph (`graph.py`)

An adjacency-list graph supporting directed/undirected and weighted edges. Five algorithms are implemented covering traversal, cycle detection, shortest paths, and ordering.

**Operations covered:**

| Method | Description | Time |
|---|---|---|
| `add_vertex(v)` | Add an isolated vertex | O(1) |
| `add_edge(u, v, weight)` | Add a weighted edge | O(1) |
| `bfs(start)` | Breadth-first traversal | O(V + E) |
| `dfs(start)` | Depth-first traversal | O(V + E) |
| `has_cycle_undirected()` | Detect cycles via DFS + parent tracking | O(V + E) |
| `dijkstra(start)` | Shortest distances from source | O((V + E) log V) |
| `topological_sort()` | DFS post-order sort (DAGs only) | O(V + E) |

#### Algorithms

**BFS — Breadth-First Search**
```
1. Create a visited set and add the start vertex
2. Create a queue and enqueue the start vertex
3. While the queue is not empty:
   a. Dequeue the front vertex
   b. Record it in the traversal order
   c. For each unvisited neighbour:
      - Mark as visited
      - Enqueue it
4. Return the traversal order
```

**DFS — Depth-First Search**
```
1. Mark the current vertex as visited
2. Record it in the traversal order
3. For each unvisited neighbour:
   a. Recursively call DFS on that neighbour
4. Return the traversal order
```

**Cycle Detection (Undirected)**
```
1. For each unvisited vertex v, call DFS-Cycle(v, parent=None):
   a. Mark v as visited
   b. For each neighbour n of v:
      - If n is not visited: recursively call DFS-Cycle(n, parent=v)
        If that call returns True, propagate True upward
      - If n is visited AND n != parent: a back edge exists → return True
   c. Return False (no cycle from this path)
2. If all vertices are exhausted without finding a cycle, return False
```

**Dijkstra's Shortest Path**
```
1. Set distance[start] = 0; set distance[all others] = infinity
2. Create a min-heap and push (0, start)
3. While the heap is not empty:
   a. Pop the vertex with the smallest distance (dist, v)
   b. If v is already visited, skip it
   c. Mark v as visited
   d. For each neighbour n of v with edge weight w:
      - new_dist = dist + w
      - If new_dist < distance[n]:
        · Update distance[n] = new_dist
        · Push (new_dist, n) onto the heap
4. Return the distances dictionary
```

**Topological Sort (DAG only)**
```
1. For each unvisited vertex v, call DFS-Topo(v):
   a. Mark v as visited
   b. For each unvisited neighbour n:
      - Recursively call DFS-Topo(n)
   c. After all neighbours are processed, push v onto the stack
2. Reverse the stack
3. Return the reversed stack as the topological order
```

**Quick example — undirected weighted graph:**
```python
g = Graph(directed=False)
g.add_edge('A', 'B', 4)
g.add_edge('A', 'C', 2)
g.add_edge('B', 'C', 5)
g.add_edge('C', 'D', 3)

print(g.bfs('A'))                    # ['A', 'B', 'C', 'D']
print(g.dijkstra('A'))               # {'A': 0, 'B': 4, 'C': 2, 'D': 5}
print(g.has_cycle_undirected())      # True
```

**Quick example — DAG topological sort:**
```python
dag = Graph(directed=True)
dag.add_edge('compile', 'link')
dag.add_edge('compile', 'test')
dag.add_edge('link', 'run')
dag.add_edge('test', 'run')
print(dag.topological_sort())
# Output: ['compile', 'test', 'link', 'run'] or valid variant
```

---

## ⚡ Complexity Cheat Sheet

| Structure | Search | Insert | Delete | Space |
|---|---|---|---|---|
| Linked List | O(n) | O(1) prepend / O(n) append | O(n) | O(n) |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(n) |
| B-Tree | O(log n) | O(log n) | — | O(n) |
| Graph — BFS/DFS | — | O(1) | — | O(V + E) |
| Graph — Dijkstra | O((V+E) log V) | — | — | O(V) |

---

## 🔑 Key Concepts to Remember

**Linked List**
- No random access — must walk from head every time
- `prepend` is O(1); `append` is O(n) without a tail pointer

**AVL Tree**
- Balance factor = left height − right height; must stay in {−1, 0, 1}
- Rotations happen on the way *back up* the recursion stack
- Delete uses the in-order successor (leftmost node of the right subtree) when removing a node with two children

**B-Tree**
- Splits happen *proactively on the way down* — no second pass needed
- Height grows only when the root splits — always balanced by design
- Preferred over BST/AVL for disk-based storage (fewer I/O operations per lookup)

**Graph**
- BFS uses a queue (FIFO); DFS uses a stack (LIFO / recursion)
- BFS gives shortest path in unweighted graphs; Dijkstra for weighted
- Dijkstra fails on negative weights — use Bellman-Ford instead
- Topological sort is only valid on DAGs (directed + acyclic)
- Cycle detection in undirected graphs requires parent tracking to avoid false positives from reverse edges

---

## ▶️ Running the Code

No external dependencies — standard library only.

```bash
python linked_list.py
python avl_tree.py
python b_tree.py
python graph.py
```

Python 3.7+ required (uses `defaultdict`, `deque`, `heapq`).

---

## 🗺️ What's Next

- [ ] Doubly linked list
- [ ] Red-Black Tree
- [ ] B-Tree deletion
- [ ] Bellman-Ford (negative weights)
- [ ] Floyd-Warshall (all-pairs shortest paths)
- [ ] Union-Find / Disjoint Set

---

## 🤖 AI Assistance Disclosure

This project was developed with AI assistance.

---

## 📄 Licence

MIT — free to use, modify, and distribute.
