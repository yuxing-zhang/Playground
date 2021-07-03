class Node():
    def __init__(self, data):
        self.data = data
        self.pre = None
        self.next = None

# LinkedList
# This class is not to be used directly
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

    # Insert at the front
    def _insert(self, x):
        if self.is_empty():
            self.head = Node(x)
        else:
            p = Node(x)
            self.head.next, self.head = p, p
        self.size += 1

    # Delete at the front
    def _delete(self):
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
        self._insert(x)

    def pop():
        return self._delete()

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
class Heap():
    def __init__(self):
        self.data = []

    def is_empty(self):
        return not self.data

    def get_size(self):
        return len(self.data)

    # Helper function to swap elements
    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    # Pop the min element and balance the heap
    def pop(self):
        if self.is_empty():
            return
        x = self.data[0]
        self.data[0] = self.data.pop()
        # Maintain heap property
        current, left = 0, _left(0)
        while left < len(self.data):
            # Find minimum between left and right children
            mini = left
            if left + 1 < len(self.data) and self.data[left + 1] <\
                    self.data[left]:
                mini += 1
            # End loop if heap property is not violated
            if self.data[current] <= self.data[mini]:
                break
            self._swap(current, mini)
            current, left = mini, _left(mini)
        return x

    # Add an element to the heap and balance it
    def push(self, x):
        self.data.append(x)
        # Maintain heap property
        current = len(self.data) - 1
        while current:
            parent = _parent(current)
            # End loop if heap property is not violated
            if self.data[parent] <= self.data[current]:
                break
            self._swap(parent, current)
            current = parent

# Union-find data structure with path compression and union by rank
class Disjoint():
    def __init__(self, n):
        # Initially every element is a disjoint set
        pre = list(range(n))
        rank = [0] * n

    # Find the set the i-th element belongs to
    def find(self, i):
        if pre[i] == i:
            return i
        # Path compression
            pre[i] = find(self, pre[i])
        rank[pre[i]] = 0
        return pre[i]

    # Union by rank
    def union(self, i, j):
        if rank[i] < rank[j]:
            pre[i] = j
        else:
            pre[j] = i
            if rank[i] == rank[j]:
                rank[i] += 1

# Graph equipped with several common algorithms
# Included algorithms:
#   Depth first search
#   Breadth first search
#   Dijkstra's shortest path algorithm
#   Floyd-Warshall algorithm for all-pairs shortest path
#   Kruskal's MST algorithm
class Graph
