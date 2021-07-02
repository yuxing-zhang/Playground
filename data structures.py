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

    def is_empty():
        return s.is_empty() and t.is_empty()

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


class Heap

class SegmentTree

class Graph
