import numpy as np

def qs(s):
    n = len(s)
    if n <= 1:
        return
    l, r = 1, n - 1
    while True:
        while l < n and s[l] <= s[0]: l += 1
        while r > 0 and s[r] >= s[0]: r -= 1
        if l > r: break
        s[l], s[r] = s[r], s[l]
    s[0], s[r] = s[r], s[0]
    qs(s[:r])
    qs(s[l:])

if __name__ == '__main__':
    s = np.random.randint(100, size=10)
    qs(s)
    print(s)
