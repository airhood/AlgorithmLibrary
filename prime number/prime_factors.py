import miller_rabin
import pollard_rho

def prime_factors(n):
    if n == 1:
        return []
    if miller_rabin(n):
        return [n]
    d = pollard_rho(n)
    return prime_factors(d) + prime_factors(n // d)