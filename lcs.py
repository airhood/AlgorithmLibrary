def lcs(arr1, arr2):
    N, M = len(arr1), len(arr2)

    arr1 = [None] + arr1
    arr2 = [None] + arr2

    dp = [[0 for _ in range(M+1)] for _ in range(N+1)]

    for i in range(1, N+1):
        for j in range(1, M+1):
            if arr1[i] == arr2[j]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[N][M]