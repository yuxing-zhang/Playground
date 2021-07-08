# The segment tree allows for efficient range queries. It requires O(n)
# extra space and O(n) preprocessing time and offers O(log n) query time.

# Helper function to get children of a node
def _left(i): return 2 * i + 1
def _right(i): return 2 * i + 2

class SegmentTree():
    def __init__(self, data, query):
        # Needs 4n space
        self.n = len(data)
        self.q = query
        self.tree = [None] * (4 * self.n)
        # Recursively build the tree
        self._build(data, query, 0, self.n, 0)

    # Build the subtree at a node with data[l:r]
    def _build(self, data, query, l, r, node):
        if r <= l:
            return
        if r == l + 1:
            self.tree[node] = data[l]
            return
        m = (l + r) // 2
        _l, _r = _left(node), _right(node)
        self._build(data, query, l, m, _l)
        self._build(data, query, m, r, _r)
        self.tree[node] = query(self.tree[_l], self.tree[_r])

    # Query at a given node
    def _query(self, start, end, query, l, r, node):
        if start >= end or start >= r or end <= l:
            return None
        if start <= l and end >= r:
            return self.tree[node]
        m = (l + r) // 2
        ql, qr = self._query(start, end, query, l, m, _left(node)),\
                 self._query(start, end, query, m, r, _right(node))
        if ql != None:
            if qr != None:
                return query(ql, qr)
            return ql
        return qr

    # Query the whole tree by querying its root
    def query(self, start, end):
        return self._query(start, end, self.q, 0, self.n, 0)
