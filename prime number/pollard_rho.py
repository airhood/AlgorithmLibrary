import miller_rabin

import math
import random

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