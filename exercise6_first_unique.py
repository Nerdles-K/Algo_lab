import unittest
from collections import OrderedDict

def first_unique_char_A(s):
    if not s: return -1
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    for i in range(len(s)):
        if freq[s[i]] == 1:
            return i
    return -1

def first_unique_char_B(s):
    if not s: return -1
    ord_freq = OrderedDict()
    for char in s:
        ord_freq[char] = ord_freq.get(char, 0) + 1
    for char, count in ord_freq.items():
        if count == 1:
            return s.find(char)
    return -1

# --- UNIT TEST CLASS ---
class TestUniqueCharFinder(unittest.TestCase):

    def setUp(self):
        """Define the functions to be tested."""
        self.functions = [first_unique_char_A, first_unique_char_B]

    def test_standard_cases(self):
        """Tests the standard examples provided in the exercise."""
        for func in self.functions:
            with self.subTest(func=func.__name__):
                self.assertEqual(func("leetcode"), 0)
                self.assertEqual(func("loveleetcode"), 2)
                self.assertEqual(func("dddccdbba"), 8)

    def test_no_unique_char(self):
        """Tests cases where no unique character exists."""
        for func in self.functions:
            with self.subTest(func=func.__name__):
                self.assertEqual(func("aabb"), -1)
                self.assertEqual(func("abcabc"), -1)

    def test_edge_cases(self):
        """Tests empty strings and single characters."""
        for func in self.functions:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(""), -1)
                self.assertEqual(func("z"), 0)

if __name__ == "__main__":
    unittest.main()