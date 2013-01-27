import unittest
from project.export_data.exportdata import ExportData
from project.test.testutils import row_map
from project.util import memoize


class ABC:
    @memoize
    def fibonacci(self, n):
        if n < 2: return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    @memoize
    def square(self, n):
        return n * n


class TestFunctions(unittest.TestCase):
    def test_fibo(self):
        a = ABC()
        self.assertEqual(55, a.fibonacci(10))
        self.assertEqual(354224848179261915075, a.fibonacci(100))

    def test_exportdata_load_row(self):
        data = ExportData()
        data._load_row('USA', 'UK', row_map(y66=4345435))
        self.assertEquals(0, data.export_data(1965, 'USA', 'UK'))
        self.assertEquals(4345435, data.export_data(1966, 'USA', 'UK'))
        self.assertEquals(0, data.export_data(1965, 'UK', 'India'))
        self.assertEquals(-1, data.export_data(1965, 'UK', 'India', return_this_for_missing_datapoint=-1))