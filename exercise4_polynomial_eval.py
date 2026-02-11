def polynomial_eval(coeffs, x):
    n = len(coeffs)
    
    if n == 0:
        return 0
    
    result = coeffs[n - 1]
    
    for i in range(n - 2, -1, -1):
        result = (result * x) + coeffs[i]
        
    return result