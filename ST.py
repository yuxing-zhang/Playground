# A clearer implementation of segment tree
class ST():
    def __init__(self, s, f):
        self.s = s
        self.n = len(s)
        # 4 * len(s) needed for worst case
        self.t = [None] * 4 * self.n
        self.f = f
        self._build(0, 0, self.n)

    @staticmethod
    def _left(x): return 2 * x + 1
    @staticmethod
    def _right(x): return 2 * x + 2

    def _build(self, x, i, j):
        if j - i == 1:
            self.t[x] = self.s[i]
            return
        l, r = self._left(x), self._right(x)
        self._build(l, i, (i+j)//2)
        self._build(r, (i+j)//2, j)
        self.t[x] = self.f(self.t[l], self.t[r])

    def query(self, i, j):
        return self._query(i, j, 0, 0, self.n)

    def _query(self, i, j, x, l, r):
        if j <= l or i >= r: return None
        if i <= l and j >= r: return self.t[x]
        lq, rq = self._query(i, j, self._left(x), l, (l+r)//2),\
                 self._query(i, j, self._right(x), (l+r)//2, r)
        if not lq: return rq
        if not rq: return lq
        return self.f(lq, rq)
