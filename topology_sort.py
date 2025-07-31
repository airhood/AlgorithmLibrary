from collections import deque

def topology_sort(N, arr, inDegree):
    result = []
    q = deque()
    for i in range(1, N+1):
        if inDegree[i] == 0:
            q.append(i)
    
    while q:
        x = q.popleft()
        result.append(x)
        for j in arr[x]:
            inDegree[j] -= 1
            if inDegree[j] == 0:
                q.append(j)
    
    if len(result) != N:
        return None
    return result