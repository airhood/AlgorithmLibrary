import numpy as np
import math
import cmath

# 재귀적으로 구현한 fft
def fft_recursive(x):
    N = len(x)
    
    if N <= 1:
        return x
    
    if N & (N - 1) != 0:
        next_power_of_2 = 1 << math.ceil(math.log2(N))
        x = x + [0] * (next_power_of_2 - N)
        return fft_recursive(x)
    
    even = fft_recursive(x[0::2])
    odd = fft_recursive(x[1::2])
    
    result = [0] * N
    
    for k in range(N // 2):
        omega = cmath.exp(-2j * math.pi * k / N)
        
        t = omega * odd[k]
        result[k] = even[k] + t
        result[k + N // 2] = even[k] - t
    
    return result

# 비트 역순 정렬을 이용해 구현한 fft
def fft(x):
    N = len(x)
    
    if N & (N - 1) != 0:
        next_power_of_2 = 1 << math.ceil(math.log2(N))
        x = x + [0] * (next_power_of_2 - N)
        N = next_power_of_2

    # 비트 역순 정렬
    j = 0
    for i in range(1, N):
        reverse = N >> 1
        while j >= reverse:
            j -= reverse
            reverse >>= 1
        j += reverse
        if i < j:
            x[i], x[j] = x[j], x[i]
    
    length = 2
    while length <= N:
        # 단위근 계산
        omega = cmath.exp(-2j * math.pi / length)
        
        # 버터플라이 연산
        for i in range(0, N, length):
            w = 1
            for j in range(length // 2):
                u = x[i + j]
                v = x[i + j + length // 2] * w
                
                x[i + j] = u + v
                x[i + j + length // 2] = u - v
                
                w *= omega
        
        length <<= 1
    
    return x

# 복소수 켤레를 이용한 ifft
def ifft(x):
    N = len(x)
    
    # 복소수 켤레
    x_conj = [complex(val).conjugate() for val in x]
    
    result = fft(x_conj)
    
    return [val.conjugate() / N for val in result]

# 페르마 소정리를 사용한 모듈러 역원 계산
def mod_inverse(a, mod):
    return pow(a, mod - 2, mod)

# fft보다 정확도를 높인 ntt(Number Theoretic Transform)
def ntt(x, inverse=False):
    MOD = 998244353 # ntt 소수
    ROOT = 3 # 원시근
    
    N = len(x)
    
    # 비트 역순 정렬
    j = 0
    for i in range(1, N):
        reverse = N >> 1
        while j >= reverse:
            j -= reverse
            reverse >>= 1
        j += reverse
        if i < j:
            x[i], x[j] = x[j], x[i]
    
    # Cooley-Tukey 알고리즘
    step = 2
    while step <= N:
        half = step >> 1
        
        # 단위근 계산
        w = pow(ROOT, (MOD - 1) // step, MOD)
        if inverse:
            w = mod_inverse(w, MOD)
        
        # 버터플라이 연산
        for i in range(0, N, step):
            w_pow = 1
            for j in range(i, i + half):
                u = x[j]
                v = (x[j + half] * w_pow) % MOD
                x[j] = (u + v) % MOD
                x[j + half] = (u - v + MOD) % MOD
                w_pow = (w_pow * w) % MOD
        
        step <<= 1

    if inverse:
        n_inv = mod_inverse(N, MOD)
        for i in range(N):
            x[i] = (x[i] * n_inv) % MOD
    
    return x

# 일반적인 합성곱 계산
def convolution_naive(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            result[i + j] += a[i] * b[j]
    return result

# ntt를 이용한 합성곱 계산
def convolution_ntt(a, b):
    result_size = len(a) + len(b) - 1
    size = 1
    while size < result_size:
        size <<= 1
    
    a_padded = a + [0] * (size - len(a))
    b_padded = b + [0] * (size - len(b))
    
    ntt_a = ntt(a_padded[:])
    ntt_b = ntt(b_padded[:])
    
    # 점별 곱셈
    MOD = 998244353
    ntt_result = [(ntt_a[i] * ntt_b[i]) % MOD for i in range(size)]
    
    result = ntt(ntt_result, inverse=True)
    
    return result[:result_size]

# ntt를 이용한 큰 수 곱셈
def multiply_large_numbers(a, b):
    # 숫자 -> 자릿수 배열
    if isinstance(a, int):
        a = [int(d) for d in str(a)[::-1]]
    if isinstance(b, int):
        b = [int(d) for d in str(b)[::-1]]
    
    result_len = len(a) + len(b) - 1
    size = 1
    while size < result_len:
        size <<= 1
    
    a_padded = a + [0] * (size - len(a))
    b_padded = b + [0] * (size - len(b))
    
    ntt_a = ntt(a_padded[:])
    ntt_b = ntt(b_padded[:])
    
    # 점별 곱셈
    MOD = 998244353
    ntt_result = [(ntt_a[i] * ntt_b[i]) % MOD for i in range(size)]
    
    result = ntt(ntt_result, inverse=True)
    
    # 자릿수 올림 처리
    carry = 0
    for i in range(len(result)):
        total = result[i] + carry
        result[i] = total % 10
        carry = total // 10
    
    # 남은 자릿수 올림 처리
    while carry:
        result.append(carry % 10)
        carry //= 10
    
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    
    return int(''.join(map(str, result[::-1])))