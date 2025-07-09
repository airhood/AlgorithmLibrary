import math

class SegmentTree:
    def __init__(self, arr, N):
        self.arr = arr
        self.tree = [0] * (2**(math.ceil(math.log2(N)+1)))

    def segment(self, left, right, i=1):
        if left == right:
            self.tree[i] = self.arr[left]
            return self.tree[i]
        
        mid = (left + right) // 2
        self.tree[i] = self.segment(left, mid, i*2) + self.segment(mid+1, right, i*2+1)
        return self.tree[i]

    def query(self, start, end, left, right, i=1):
        if end < left or start > right:
            return 0
        
        if left <= start and end <= right:
            return self.tree[i]
        
        mid = (start + end) // 2
        return self.query(start, mid, left, right, i*2) + self.query(mid+1, end, left, right, i*2+1)
    
    def update(self, start, end, idx, val, i=1):
        if start > idx or idx > end:
            return self.tree[i]
        
        if start == end:
            self.tree[i] = val
            return self.tree[i]
        
        mid = (start + end) // 2
        self.tree[i] = self.update(start, mid, idx, val, i*2) + self.update(mid+1, end, idx, val, i*2+1)
        return self.tree[i]
