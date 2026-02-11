import unittest

def polynomial_eval(coeffs, x):
    n = len(coeffs)
    
    if n == 0:
        return 0
    
    result = coeffs[n - 1]
    
    for i in range(n - 2, -1, -1):
        result = (result * x) + coeffs[i]
        
    return result
class TestPolynomialEval(unittest.TestCase):

    def test_image_example(self):
        self.assertEqual(polynomial_eval([3, -2, 0, 5], 2.0), 39.0)

    def test_linear(self):
        self.assertEqual(polynomial_eval([1, 2], 3.0), 7.0)

    def test_empty(self):
        self.assertEqual(polynomial_eval([], 10), 0)

    def test_negative_x(self):
        self.assertEqual(polynomial_eval([3, -2], -1), 5)

if __name__ == '__main__':
    unittest.main()