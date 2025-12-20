class DSU:
    def __init__(self, n: int):
        self.par = list(range(n))
        self.size = [1] * n

    def get(self, x: int) -> int:
        while self.par[x] != x:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x

    def merge(self, a: int, b: int) -> None:
        a = self.get(a)
        b = self.get(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        # size[a] >= size[b]
        self.par[b] = a
        self.size[a] += self.size[b]
        return
