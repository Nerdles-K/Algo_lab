import unittest

def integer_mirror(n):
    rev = 0
    if n == 0:
        return 0
    while(n > 0):
        a = n % 10
        rev = rev * 10 + a
        n = n // 10
    return rev

class TestIntegerMirror(unittest.TestCase):

    def test_standard_reversal(self):
        self.assertEqual(integer_mirror(315), 513)

    def test_trailing_zeros(self):
        # Requirement: 400 -> 4
        self.assertEqual(integer_mirror(400), 4)

    def test_single_digit(self):
        self.assertEqual(integer_mirror(7), 7)

    def test_zero(self):
        self.assertEqual(integer_mirror(0), 0)

    def test_large_number(self):
        self.assertEqual(integer_mirror(123456789), 987654321)

if __name__ == '__main__':
    unittest.main()