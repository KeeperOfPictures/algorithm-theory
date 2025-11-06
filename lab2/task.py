def fast_multiply(m, n):
    result = 0
    while n > 0:
        if n & 1:
            result += m
        m <<= 1
        n >>= 1
    return result

def fast_square(m):
    if m == 0:
        return 0
    
    n = abs(m)
    result = 0
    temp = n
    
    while temp > 0:
        if temp & 1:
            result += n
        n <<= 1
        temp >>= 1
    
    return result if m >= 0 else result

def fast_power(base, exponent):
    if exponent == 0:
        return 1
    if exponent == 1:
        return base
    
    # Для отрицательных степеней
    if exponent < 0:
        return 1 / fast_power(base, -exponent)
    
    result = 1
    current = base
    
    while exponent > 0:
        if exponent & 1:  # если степень нечетная
            result *= current
        current *= current  # возводим в квадрат
        exponent >>= 1     # делим степень на 2
    
    return result

def nth_root_newton(number, n, precision=1e-10):
    if number < 0 and n % 2 == 0:
        raise ValueError("Четный корень из отрицательного числа")
    if n == 0:
        raise ValueError("Нулевая степень корня")
    
    if number >= 0:
        x = number / n
    else:
        x = -abs(number) / n
    
    while True:
        x_new = ((n - 1) * x + number / (x ** (n - 1))) / n
        
        if abs(x_new - x) < precision:
            return x_new
        x = x_new


print(fast_multiply(13, 17)) # 221
print(fast_power(2, 10)) # 1024
print(fast_power(3, 5)) # 243
print(nth_root_newton(27, 3))
print(nth_root_newton(16, 4))