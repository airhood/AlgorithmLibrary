import math

def seive(n):
    is_prime = [1] * (n+1)
    is_prime[0] = 0
    is_prime[1] = 0

    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i**2, n+1, i):
                is_prime[j] = 0

    primes = [i for i, val in enumerate(is_prime) if val == 1]
    return primes