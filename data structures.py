class Node():
    def __init__(self, data):
        self.data = data
        self.pre = None
        self.next = None

# LinkedList
class List():
    def __init__(self):
        self.head = None
        self.size = 0

    # String representation
    def __str__(self):
        s = ''
        p = head
        while p:
            s += '%s -> ' % str(p.data)
            p = p.next
        return s[:-4]

    def is_empty(self):
        return not self.size

    def get_size(self):
        return self.size

    def insert(self, x):
        if self.is_empty():
            self.head = Node(x)
        else:
            p = Node(x)
            self.head.next, self.head = p, p
        self.size += 1

    def delete(self):
        if self.is_empty():
            return
        p = self.head
        self.head = p.next
        self.size -= 1
        return p.data

# Stack based on LinkedList
class Stack(List):
    def __init__(self):
        super(Stack, self).__init__()

    def push(self, x):
        self.insert(x)

    def pop():
        return self.delete()

    # Check the head element
    def peek(self):
        if self.is_empty():
            return
        return self.head.data

# Queue implemented with 2 stacks
class Queue():
    def __init__(self):
        self.s, self.t = Stack(), Stack()

    def __str__():
        s, t = str(self.s), str(self.t)
        # When s and t are both non-empty, add a link between them
        if s and t:
            return s + ' -> ' t
        return s + t

    def is_empty():
        return s.is_empty() and t.is_empty()

    def get_size():
        return s.get_size() + t.get_size()

    # Enqueue by pushing to stack s
    def enqueue(self, x):
        self.s.push(x)

    # Dequeue by poping from stack t
    def dequeue(self):
        if t.is_empty():
            if s.is_empty():
                return
            # Reverse move s to t when t is empty
            while not s.is_empty():
                t.push(s.pop())
        return t.pop()

    # Check the front element of the queue
    def peek(self):
        if t.is_empty():
            if s.is_empty():
                return
            # Reverse move s to t when t is empty
            while not s.is_empty():
                t.push(s.pop())
        return t.peek()

# Helper functions to get parent and child index in binary heap
def _parent(x):
    if x == 0:
        return x
    return (x - 1) // 2

def _left(x):
    return 2 * x + 1

def _right(x):
    return 2 * x + 2

# Min-heap implemented as a binary heap
# Elements are (key, value) pairs to facilitate implementation of
# Dijkstra's algorithm later
class Heap():
    def __init__(self):
        self.data = []
        # Index maps value to its index
        self.index = {}

    def is_empty(self):
        return not self.data

    def get_size(self):
        return len(self.data)

    # Return the key of a given value
    def get_key(self, value):
        return self.data[self.index[value]][0]

    # Helper function to swap elements
    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.index[self.data[i][1]] = j
        self.index[self.data[j][1]] = i

    def pop(self):
        if self.is_empty():
            return
        x = self.data[0]
        del self.index[x[1]]
        self.data[0] = self.data.pop()
        self.index[self.data[0][1]] = 0
        # Maintain heap property
        current, left = 0, _left(0)
        while left < len(self.data):
            # Find minimum between left and right children
            mini = left
            if left + 1 < len(self.data) and self.data[left + 1][0] <\
                    self.data[left][0]:
                mini += 1
            # End loop if heap property is not violated
            if self.data[current][0] <= self.data[mini][0]:
                break
            self._swap(current, mini)
            current, left = mini, _left(mini)
        return x

    def push(self, x):
        self.data.append(x)
        self.index[x[1]] = len(self.data) - 1
        # Maintain heap property
        current = len(self.data) - 1
        while current:
            parent = _parent(current)
            # End loop if heap property is not violated
            if self.data[parent][0] <= self.data[current][0]:
                break
            self._swap(parent, current)
            current = parent

    # Decrease the key of an value and balance the heap
    # The new key must be smaller than the original key
    def decrease_key(self, value, key):
        current = self.index[value]
        self.data[current][0] = key
        while current:
            parent = _parent(current)
            if self.data[parent][0] <= self.data[current][0]:
                break
            self._swap(parent, current)
            current = parent

# Union-find data structure with path compression and union by rank
class Disjoint():
    def __init__(self, n):
        # Initially every element is a disjoint set
        pre = list(range(n))
        rank = [0] * n

    def find(self, i):
        if pre[i] == i:
            return i
        # Path compression
        pre[i] = find(self, pre[i])
        return pre[i]

    # Union by rank
    def union(self, i, j):
        i, j = self.find(i), self.find(j)
        if rank[i] < rank[j]:
            pre[i] = j
        else:
            pre[j] = i
            # Increase rank only when two sets are of equal rank
            if rank[i] == rank[j]:
                rank[i] += 1

# Undirected graph equipped with several common algorithms
# Included algorithms:
#   Depth first search
#   Breadth first search
#   Dijkstra's shortest path algorithm
#   Floyd-Warshall algorithm for all-pairs shortest path
#   Kruskal's MST algorithm
class Graph:
    # Graph initialization specified by # of its vertices
    def __init__(self, n):
        self.V = [[] for _ in range(n)]
        self.E = {}
        self.n = n

    # Add edge (u, v) with weight w
    def add_edge(self, u, v, w):
        self.V[u].append(v)
        self.V[v].append(u)
        self.E[(u, v)] = self.E[(v, u)] = w

    # Recursively apply function f to vertices in a connected component
    def _dfs(self, u, f, visited): 
        visited[u] = True
        f(u)
        for v in self.V[u]:
            if not visited(v):
                self._dfs(v, f, visited)

    # Traverse the graph with dfs
    def dfs(self, f):
        visited = [False] * self.n
        for u in self.V:
            if not visited[u]:
                self._dfs(u, f, visited)

    # Traverse a connected component with bfs
    def _bfs(self, u, f, visited):
        q = Queue()
        q.enqueue(u)
        visited[u] = True
        while q:
            u = q.dequeu()
            f(u)
            for v in self.V[u]:
                if not visited[v]:
                    q.enqueue(v)
                    visited[v] = True

    # Traverse the graph with bfs
    def bfs(self, f):
        visited = [False] * self.n
        for v in self.V:
            if not visited[v]:
                self._bfs(v, f, visited)

    # Find the shortest path between vertex u and all other vertices,
    # assuming connectivity of the graph
    def dijkstra(self, u):
        h = Heap()
        visited = [False] * self.n
        # Initialize heap with (0, u) and (inf, v) for v != u
        for v in range(self.n):
            h.push((float('inf'), v))
        h.decrease_key(u, 0)
        # Initialize all lengths to inf and previous vertex to -1
        dist = [float('inf')] * self.n
        dist[u] = 0
        pre = [-1] * self.n
        while h:
            k, u = h.pop()
            visited[u] = True
            for v in self.V[u]:
                # Only check neighbors that are in the heap
                if not visited[v] and k + self.E[(u, v)] < h.get_key(v):
                    dist[v] = k + self.E[(u, v)]
                    h.decrease_key(v, dist[v])
                    pre[v] = u
        return dist, pre

    def fw(self):
        

    # Kruskal's algorithm to find a minimum spanning tree
    # The MST is represented by a set of edges
    def kruskal(self):
        # self.E contains two copies of each edge
        # Only one copy is needed
        edges = sorted([e for e in self.E if e[0] < e[1]],
                key=lambda x: self.E[x])
        mst = []
        sets = Disjoint(self.n)
        for e in edges:
            # Find the lightest edge connecting two disjoint components
            if sets.find(e[0]) != self.find(e[1]):
                sets.union(*e)
                mst.append(e)
        return mst











