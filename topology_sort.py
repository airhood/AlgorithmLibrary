from queue import Queue

def topology_sort(N, arr, inDegree):
    result = []
    q = Queue()
    for i in range(1, N+1):
        if inDegree[i] == 0:
            q.put(i)
    while not q.empty():
        x = q.get()
        result.append(x)
        for j in arr[x]:
            inDegree[j] -= 1
            if inDegree[j] == 0:
                q.put(j)
    return result