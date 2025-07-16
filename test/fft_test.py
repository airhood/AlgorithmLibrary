from fft import fft_recursive, fft, ifft, ntt, convolution_naive, convolution_ntt, multiply_large_numbers

import numpy as np
import math
import cmath
import time
import random

# 테스트 함수들
def test_fft_accuracy():
    """FFT 정확성 테스트"""
    print("=" * 50)
    print("FFT 정확성 테스트")
    print("=" * 50)
    
    # 테스트 데이터 생성
    test_cases = [
        [1, 2, 3, 4],
        [1, 0, 1, 0],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [1] * 16,
        [i for i in range(32)]
    ]
    
    for i, data in enumerate(test_cases):
        print(f"\n테스트 케이스 {i+1}: {data[:8]}{'...' if len(data) > 8 else ''}")
        
        # NumPy FFT
        numpy_result = np.fft.fft(data)
        
        # 당신의 FFT 구현들
        recursive_result = fft_recursive(data[:])
        iterative_result = fft(data[:])
        
        # 길이 맞추기 (2의 거듭제곱으로 패딩)
        padded_len = 1
        while padded_len < len(data):
            padded_len <<= 1
        
        # 오차 계산
        recursive_error = np.mean(np.abs(numpy_result[:padded_len] - recursive_result[:padded_len]))
        iterative_error = np.mean(np.abs(numpy_result[:padded_len] - iterative_result[:padded_len]))
        
        print(f"  NumPy FFT: {numpy_result[:4]}...")
        print(f"  재귀 FFT:  {recursive_result[:4]}...")
        print(f"  반복 FFT:  {iterative_result[:4]}...")
        print(f"  재귀 오차: {recursive_error:.2e}")
        print(f"  반복 오차: {iterative_error:.2e}")
        print(f"  정확도: {'✓' if recursive_error < 1e-10 and iterative_error < 1e-10 else '✗'}")

def test_ifft_accuracy():
    """IFFT 정확성 테스트"""
    print("\n" + "=" * 50)
    print("IFFT 정확성 테스트")
    print("=" * 50)
    
    test_cases = [
        [1, 2, 3, 4],
        [1, 0, 1, 0],
        [1, 2, 3, 4, 5, 6, 7, 8]
    ]
    
    for i, data in enumerate(test_cases):
        print(f"\n테스트 케이스 {i+1}: {data}")
        
        # FFT -> IFFT로 원본 복원 테스트
        fft_result = fft(data[:])
        ifft_result = ifft(fft_result)
        
        # NumPy와 비교
        numpy_fft = np.fft.fft(data)
        numpy_ifft = np.fft.ifft(numpy_fft)
        
        # 오차 계산
        recovery_error = np.mean(np.abs(np.array(data) - np.array(ifft_result[:len(data)])))
        numpy_error = np.mean(np.abs(numpy_ifft[:len(data)] - np.array(ifft_result[:len(data)])))
        
        print(f"  원본:      {data}")
        print(f"  복원:      {[round(x.real, 6) for x in ifft_result[:len(data)]]}")
        print(f"  NumPy:     {[round(x.real, 6) for x in numpy_ifft[:len(data)]]}")
        print(f"  복원 오차: {recovery_error:.2e}")
        print(f"  NumPy 오차: {numpy_error:.2e}")
        print(f"  정확도: {'✓' if recovery_error < 1e-10 and numpy_error < 1e-10 else '✗'}")

def test_convolution_accuracy():
    """컨볼루션 정확성 테스트"""
    print("\n" + "=" * 50)
    print("컨볼루션 정확성 테스트")
    print("=" * 50)
    
    test_cases = [
        ([1, 2, 3], [4, 5, 6]),
        ([1, 0, 1], [1, 1, 1]),
        ([2, 3, 1], [1, 4, 2]),
        ([1, 2, 3, 4], [5, 6, 7, 8])
    ]
    
    for i, (a, b) in enumerate(test_cases):
        print(f"\n테스트 케이스 {i+1}: {a} * {b}")
        
        # 다양한 방법으로 컨볼루션 계산
        naive_result = convolution_naive(a, b)
        ntt_result = convolution_ntt(a, b)
        numpy_result = np.convolve(a, b).tolist()
        
        print(f"  Naive:  {naive_result}")
        print(f"  NTT:    {ntt_result}")
        print(f"  NumPy:  {numpy_result}")
        
        # 정확성 검증
        naive_match = naive_result == numpy_result
        ntt_match = ntt_result == numpy_result
        
        print(f"  Naive 정확도: {'✓' if naive_match else '✗'}")
        print(f"  NTT 정확도:   {'✓' if ntt_match else '✗'}")

def test_large_number_multiplication():
    """큰 수 곱셈 테스트"""
    print("\n" + "=" * 50)
    print("큰 수 곱셈 테스트")
    print("=" * 50)
    
    test_cases = [
        (123, 456),
        (12345, 67890),
        (123456789, 987654321),
        (10**50 + 1, 10**50 + 2),
        (int('1' * 100), int('2' * 100))
    ]
    
    for i, (a, b) in enumerate(test_cases):
        print(f"\n테스트 케이스 {i+1}:")
        if len(str(a)) > 20:
            print(f"  a = {str(a)[:20]}...({len(str(a))}자리)")
            print(f"  b = {str(b)[:20]}...({len(str(b))}자리)")
        else:
            print(f"  a = {a}")
            print(f"  b = {b}")
        
        # 내장 곱셈과 NTT 곱셈 비교
        builtin_result = a * b
        ntt_result = multiply_large_numbers(a, b)
        
        match = builtin_result == ntt_result
        print(f"  내장 곱셈: {str(builtin_result)[:50]}{'...' if len(str(builtin_result)) > 50 else ''}")
        print(f"  NTT 곱셈:  {str(ntt_result)[:50]}{'...' if len(str(ntt_result)) > 50 else ''}")
        print(f"  정확도: {'✓' if match else '✗'}")

def test_performance():
    """성능 테스트"""
    print("\n" + "=" * 50)
    print("성능 테스트")
    print("=" * 50)
    
    sizes = [64, 256, 1024, 4096]
    
    for size in sizes:
        print(f"\n크기 {size} 테스트:")
        
        # 랜덤 데이터 생성
        data = [random.randint(0, 100) for _ in range(size)]
        
        # NumPy FFT
        start = time.time()
        numpy_result = np.fft.fft(data)
        numpy_time = time.time() - start
        
        # 당신의 FFT 재귀
        start = time.time()
        try:
            recursive_result = fft_recursive(data[:])
            recursive_time = time.time() - start
        except RecursionError:
            recursive_time = float('inf')
            print("  재귀 FFT: 스택 오버플로우!")
        
        # 당신의 FFT 반복
        start = time.time()
        iterative_result = fft(data[:])
        iterative_time = time.time() - start
        
        print(f"  NumPy FFT:  {numpy_time:.6f}초")
        if recursive_time != float('inf'):
            print(f"  재귀 FFT:   {recursive_time:.6f}초 ({recursive_time/numpy_time:.1f}배)")
        print(f"  반복 FFT:   {iterative_time:.6f}초 ({iterative_time/numpy_time:.1f}배)")
        
        # 컨볼루션 성능 테스트 (작은 크기만)
        if size <= 256:
            a = data[:size//2]
            b = data[size//2:]
            
            # Naive 컨볼루션
            start = time.time()
            naive_conv = convolution_naive(a, b)
            naive_time = time.time() - start
            
            # NTT 컨볼루션
            start = time.time()
            ntt_conv = convolution_ntt(a, b)
            ntt_time = time.time() - start
            
            # NumPy 컨볼루션
            start = time.time()
            numpy_conv = np.convolve(a, b)
            numpy_conv_time = time.time() - start
            
            print(f"  Naive 컨볼루션: {naive_time:.6f}초")
            print(f"  NTT 컨볼루션:   {ntt_time:.6f}초 ({naive_time/ntt_time:.1f}배 빠름)")
            print(f"  NumPy 컨볼루션: {numpy_conv_time:.6f}초")

def test_edge_cases():
    """엣지 케이스 테스트"""
    print("\n" + "=" * 50)
    print("엣지 케이스 테스트")
    print("=" * 50)
    
    # 빈 배열
    print("빈 배열 테스트:")
    try:
        result = fft([])
        print(f"  결과: {result}")
    except Exception as e:
        print(f"  오류: {e}")
    
    # 길이 1
    print("\n길이 1 테스트:")
    result = fft([5])
    print(f"  결과: {result}")
    
    # 2의 거듭제곱이 아닌 길이
    print("\n2의 거듭제곱이 아닌 길이 테스트:")
    for length in [3, 5, 7, 10]:
        data = list(range(length))
        result = fft(data)
        print(f"  길이 {length}: {len(result)} (패딩됨)")
    
    # 큰 값들
    print("\n큰 값 테스트:")
    large_data = [10**6, 10**7, 10**8, 10**9]
    ntt_result = ntt(large_data)
    print(f"  NTT 결과: {ntt_result[:4]}...")

def run_all_tests():
    """모든 테스트 실행"""
    print("FFT/NTT 구현 종합 테스트")
    print("=" * 50)
    
    test_fft_accuracy()
    test_ifft_accuracy()
    test_convolution_accuracy()
    test_large_number_multiplication()
    test_performance()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("테스트 완료!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()