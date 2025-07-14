def lower_bound(arr, x):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < x:
            left = mid + 1
        else:
            right = mid
    return left

def lis(arr):
    tail = []
    tail_idx = []
    prev_idx = [-1] * len(arr)

    for i in range(len(arr)):
        idx = lower_bound(tail, arr[i])

        if idx == len(tail):
            tail.append(arr[i])
            tail_idx.append(i)
        else:
            tail[idx] = arr[i]
            tail_idx[idx] = i

        if idx != 0:
            prev_idx[i] = tail_idx[idx - 1]

    lis = []

    track = tail_idx[-1]
    while track != -1:
        lis.append(arr[track])
        track = prev_idx[track]

    lis.reverse()

    return lis