import math

class LisSegmentTree:
    def __init__(self, N):
        self.tree = [0] * (2**(math.ceil(math.log2(N)+1)))

    def query(self, start, end, left, right, i=1):
        if end < left or start > right:
            return 0
        
        if left <= start and end <= right:
            return self.tree[i]
        
        mid = (start + end) // 2
        return max(self.query(start, mid, left, right, i*2), self.query(mid+1, end, left, right, i*2+1))
    
    def update(self, start, end, idx, val, i=1):
        if start > idx or idx > end:
            return self.tree[i]
        
        if start == end:
            self.tree[i] = val
            return self.tree[i]
        
        mid = (start + end) // 2
        self.tree[i] = max(self.update(start, mid, idx, val, i*2), self.update(mid+1, end, idx, val, i*2+1))
        return self.tree[i]
    
    def getTree(self):
        return self.tree

def lis(arr):
    N = len(arr)
    arr_s = []
    for i in range(N):
        arr_s.append((arr[i], i))
    arr_s.sort(key=lambda x:(x[0], -x[1]))
    segment_tree = LisSegmentTree(N)
    for i in range(N):
        idx = arr_s[i][1]
        max_val = 0
        if idx != 0:
            max_val = segment_tree.query(0, N-1, 0, idx)
        segment_tree.update(0, N-1, idx, max_val+1)
    return segment_tree.getTree()[1]