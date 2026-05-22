# ============================================================
#  GRAPH — Full Implementation in Python
#  Adjacency list representation — efficient for sparse graphs
#
#  Covers:
#    - Undirected and directed (digraph) edges
#    - Weighted edges
#    - BFS and DFS traversal
#    - Cycle detection (undirected)
#    - Dijkstra's shortest path (non-negative weights)
#    - Topological sort (DAGs only)
# ============================================================

import heapq                            # Min-heap for Dijkstra's priority queue
from collections import deque, defaultdict


class Graph:

    # --------------------------------------------------------
    # __init__()
    # Uses an adjacency list: a dict mapping each vertex to a
    # list of (neighbour, weight) tuples.
    # Unweighted edges default to weight 1.
    # directed=False means every edge is stored in both directions.
    # --------------------------------------------------------
    def __init__(self, directed=False):
        self.adj = defaultdict(list)    # vertex -> [(neighbour, weight), ...]
        self.directed = directed
        self.vertices = set()           # Tracks all vertices (including isolated)

    # --------------------------------------------------------
    # add_vertex() — Register a vertex with no edges yet.
    # Useful for isolated nodes that won't appear via add_edge.
    # Time: O(1)
    # --------------------------------------------------------
    def add_vertex(self, v):
        self.vertices.add(v)
        if v not in self.adj:
            self.adj[v] = []            # Ensure it appears in the adjacency list

    # --------------------------------------------------------
    # add_edge() — Connect two vertices.
    # For undirected graphs both directions are stored so
    # traversals can move freely in either direction.
    # Time: O(1)
    # --------------------------------------------------------
    def add_edge(self, u, v, weight=1):
        self.vertices.update([u, v])
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))  # Reverse edge for undirected

    # --------------------------------------------------------
    # display() — Print the adjacency list.
    # --------------------------------------------------------
    def display(self):
        print("Adjacency List:")
        for vertex in sorted(self.vertices):
            neighbours = ', '.join(f"{n}(w={w})" for n, w in self.adj[vertex])
            print(f"  {vertex} -> [{neighbours}]")

    # --------------------------------------------------------
    # bfs() — Breadth-First Search
    # Explores layer by layer using a FIFO queue.
    # Visits all vertices at distance k before moving to k+1.
    # Guarantees shortest path in UNWEIGHTED graphs.
    # Time: O(V + E)  |  Space: O(V)
    # --------------------------------------------------------
    def bfs(self, start):
        visited = set()           # Prevents revisiting vertices (and infinite loops)
        queue = deque([start])    # FIFO queue — processes level by level
        visited.add(start)
        order = []

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbour, _ in self.adj[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return order

    # --------------------------------------------------------
    # dfs() — Depth-First Search
    # Dives as deep as possible along each branch before
    # backtracking. Uses recursion (implicit call stack).
    # Foundation for cycle detection, topological sort,
    # and connected component discovery.
    # Time: O(V + E)  |  Space: O(V) for the recursion stack
    # --------------------------------------------------------
    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()       # Fresh set on the first call only
        visited.add(start)
        order = [start]

        for neighbour, _ in self.adj[start]:
            if neighbour not in visited:
                order += self.dfs(neighbour, visited)  # Recurse deeper

        return order

    # --------------------------------------------------------
    # has_cycle_undirected() — Cycle detection for undirected graphs.
    # A cycle exists if DFS reaches a visited vertex that is NOT
    # the direct parent of the current vertex.
    #
    # Why parent tracking? In an undirected graph, edge A-B is
    # stored as both A->B and B->A. Without tracking the parent,
    # B->A would always look like a "back edge" — a false cycle.
    # Time: O(V + E)
    # --------------------------------------------------------
    def has_cycle_undirected(self):
        visited = set()

        def dfs_cycle(v, parent):
            visited.add(v)
            for neighbour, _ in self.adj[v]:
                if neighbour not in visited:
                    if dfs_cycle(neighbour, v):
                        return True
                elif neighbour != parent:   # Back edge — cycle found
                    return True
            return False

        # Run from every vertex to cover disconnected components
        for v in self.vertices:
            if v not in visited:
                if dfs_cycle(v, None):
                    return True
        return False

    # --------------------------------------------------------
    # dijkstra() — Shortest path from a single source.
    # Greedy algorithm: always expands the nearest unvisited
    # vertex using a min-heap (priority queue).
    #
    # Relaxation: if a shorter path to a neighbour is found
    # via the current vertex, update it and push to the heap.
    #
    # IMPORTANT: only works correctly on non-negative edge weights.
    # For negative weights, use Bellman-Ford instead.
    # Time: O((V + E) log V)  |  Space: O(V)
    # --------------------------------------------------------
    def dijkstra(self, start):
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        heap = [(0, start)]         # (distance, vertex) — min-heap by distance
        visited = set()

        while heap:
            dist, vertex = heapq.heappop(heap)  # Extract nearest unvisited vertex

            if vertex in visited:
                continue            # Already found the shortest path to this vertex
            visited.add(vertex)

            for neighbour, weight in self.adj[vertex]:
                new_dist = dist + weight
                if new_dist < distances[neighbour]:  # Relaxation step
                    distances[neighbour] = new_dist
                    heapq.heappush(heap, (new_dist, neighbour))

        return distances

    # --------------------------------------------------------
    # topological_sort() — Valid only on DAGs.
    # Orders vertices so every directed edge u->v has u before v.
    #
    # Method: DFS post-order.
    # A vertex is pushed to the stack AFTER all its descendants
    # are processed — meaning dependencies always come first.
    # Reversing the post-order stack gives topological order.
    #
    # IMPORTANT: a cycle makes topological sort impossible.
    # Time: O(V + E)  |  Space: O(V)
    # --------------------------------------------------------
    def topological_sort(self):
        visited = set()
        stack = []

        def dfs_topo(v):
            visited.add(v)
            for neighbour, _ in self.adj[v]:
                if neighbour not in visited:
                    dfs_topo(neighbour)
            stack.append(v)     # Push AFTER all descendants are processed

        for v in self.vertices:
            if v not in visited:
                dfs_topo(v)

        return stack[::-1]      # Reverse post-order = topological order


# ============================================================
#  DRIVER CODE
# ============================================================

if __name__ == "__main__":

    # --- Undirected weighted graph ---
    print("=== Undirected Weighted Graph ===")
    g = Graph(directed=False)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 5)
    g.add_edge('B', 'D', 10)
    g.add_edge('C', 'D', 3)
    g.display()

    print("\nBFS from A:", g.bfs('A'))
    # Output: ['A', 'B', 'C', 'D']

    print("DFS from A:", g.dfs('A'))
    # Output: ['A', 'B', 'C', 'D'] (order may vary by adjacency list)

    print("Has cycle:", g.has_cycle_undirected())
    # Output: True (A-B-C-A forms a cycle)

    print("Dijkstra from A:", g.dijkstra('A'))
    # Output: {'A': 0, 'B': 4, 'C': 2, 'D': 5}
    # Shortest to D: A->C (2) + C->D (3) = 5

    # --- Directed Acyclic Graph — topological sort ---
    print("\n=== DAG — Topological Sort ===")
    dag = Graph(directed=True)
    dag.add_edge('compile', 'link')
    dag.add_edge('compile', 'test')
    dag.add_edge('link', 'run')
    dag.add_edge('test', 'run')
    dag.display()

    print("\nTopological sort:", dag.topological_sort())
    # Output: ['compile', 'link', 'test', 'run'] or valid variant
    # 'compile' must always appear before 'link', 'test', and 'run'
