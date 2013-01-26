import unittest
from project.util import memoize


class ABC:
    @memoize
    def fibonacci(self, n):
        if n < 2: return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    @memoize
    def square(self, n):
        return n * n


class TestSequenceFunctions(unittest.TestCase):
    def test_fibo(self):
        a = ABC()
        self.assertEqual(55, a.fibonacci(10))
        self.assertEqual(354224848179261915075, a.fibonacci(100))