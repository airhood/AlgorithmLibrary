N = 10

parent = [i for i in range(N+1)]

def find(x):
    y = x
    while y != parent[y]:
        y = parent[y]
    parent[x] = y
    return y

def union(x, y):
    parent_x = find(x)
    parent_y = find(y)
    if parent_x == parent_y: return
    elif parent_x > parent_y:
        parent[parent_x] = parent_y
    else:
        parent[parent_y] = parent_x