import math
import random

def miller_rabin(n):
    if n < 2:
        return False
    
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0:
            return n == p
        
    d = n - 1
    r = 0
    
    while d % 2 == 0:
        d //= 2
        r += 1

    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        found = False
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == (n-1):
                found = True
                break
        if not found:
            return False
    
    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    if miller_rabin(n):
        return n
    
    while True:
        x = random.randrange(2, n)
        y = x
        c = random.randrange(1, n)
        d = 1

        def f(x, c, n):
            return (x*x + c) % n
        
        while d == 1:
            x = f(x, c, n)
            y = f(f(y, c, n), c, n)
            d = math.gcd(abs(x - y), n)
        
        if d != n:
            if miller_rabin(d):
                return d
            else:
                return pollard_rho(d)

def prime_factors(n):
    if n == 1:
        return []
    if miller_rabin(n):
        return [n]
    d = pollard_rho(n)
    return prime_factors(d) + prime_factors(n // d)