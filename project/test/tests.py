import unittest
from project.export_data.exportdata import ExportData
from project.test.testutils import row_map, write_to_file
from project.util import memoize
import tempfile


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


    def test_exportdata_load_file(self):
        f = tempfile.NamedTemporaryFile()
        write_to_file(f,
            'ICode,Importer,ECode,Exporter,Value62,Value63,Value64,Value65,Value66,Value67,Value68,Value69,Value70,Value71,Value72,Value73,Value74,Value75,Value76,Value77,Value78,Value79,Value80,Value81,Value82,Value83,Value84,Value85,Value86,Value87,Value88,Value89,Value90,Value91,Value92,Value93,Value94,Value95,Value96,Value97,Value98,Value99,Value00',
            '"100000","World","117100","South Africa",1137424,1253225,1315703,1453614,1719904,1934726,2073399,2172388,2067276,2087840,2197399,3035278,4473097,5151976,5786599,7168917,8039418,10691282,12774748,31497500,9593869,8498300,27745267,11587906,12944273,12142881,14767609,15973854,16353354,16153549,30129310,27374820,30949042,33215626,28668008,35065432,30622443,31679773,38330367',
            '"100000","World","100000","World",130820766,144752269,163401432,178619568,196373987,206306598,229438483,261773445,301725595,336632436,394429429,547697681,822593098,860894299,967082574,1080137888,1187499282,1588616996,1927615343,1908925277,1753041348,1650817500,1875030686,1949413915.813,2097956459,2454677596,2798583134,3044659532,3471060661,3600841444,3860180402,3796916610,4305600574,5136222078,5475815227,5631902195,5575802767,5791258924,6568385296')
        d = ExportData()
        d.load_file(f.name, should_read_world_datapoints=True)
        self.assertEquals(1253225, d.export_data(1963, 'South Africa', 'World'))
        self.assertEquals(d.total_exports('South Africa', 1963), d.export_data(1963, 'South Africa', 'World'))

    def test_exportdata_percentage(self):
        f = tempfile.NamedTemporaryFile()
        write_to_file(f,
            'ICode,Importer,ECode,Exporter,Value62,Value63,Value64,Value65,Value66,Value67,Value68,Value69,Value70,Value71,Value72,Value73,Value74,Value75,Value76,Value77,Value78,Value79,Value80,Value81,Value82,Value83,Value84,Value85,Value86,Value87,Value88,Value89,Value90,Value91,Value92,Value93,Value94,Value95,Value96,Value97,Value98,Value99,Value00',
            '"100000","World","117100","South Africa",1137424,1253225,1315703,1453614,1719904,1934726,2073399,2172388,2067276,2087840,2197399,3035278,4473097,5151976,5786599,7168917,8039418,10691282,12774748,31497500,9593869,8498300,27745267,11587906,12944273,12142881,14767609,15973854,16353354,16153549,30129310,27374820,30949042,33215626,28668008,35065432,30622443,31679773,38330367',
            '"100000","World","100000","World",130820766,144752269,163401432,178619568,196373987,206306598,229438483,261773445,301725595,336632436,394429429,547697681,822593098,860894299,967082574,1080137888,1187499282,1588616996,1927615343,1908925277,1753041348,1650817500,1875030686,1949413915.813,2097956459,2454677596,2798583134,3044659532,3471060661,3600841444,3860180402,3796916610,4305600574,5136222078,5475815227,5631902195,5575802767,5791258924,6568385296',
            '"218400","USA","117100","South Africa",251562,254890,NaN,225124,250540,228294,255674,247306,290816,287973,NaN,NaN,657842,926241,1013444,1336176,2538904,2798597,3562230,2754026,2120687,2157953,2651509,2218343,2503722,1436099,1633206,1664480,1861072,1879078,1906935,2037416,2274562,2438873,2586155,2838329,3389674,3530854,4646342')
        d = ExportData()
        d.load_file(f.name, should_read_world_datapoints=True)
        self.assertEquals(0.20338726086696324, d.export_data_as_percentage(1963, 'South Africa', 'USA'))
        self.assertEquals(None, d.export_data_as_percentage(1964, 'South Africa', 'USA', True))
        self.assertEquals(0, d.export_data_as_percentage(1964, 'South Africa', 'India'))
        #        To-do:make sure if this assertion should pass for an expected value of -10 too
        self.assertEquals(-1,
            d.export_data_as_percentage(1964, 'South Africa', 'India', return_this_for_missing_datapoint=-1))

    def test_exportdata_total_exports_between_C1_andC2(self):
        f = tempfile.NamedTemporaryFile()
        write_to_file(f,
            'ICode,Importer,ECode,Exporter,Value62,Value63,Value64,Value65,Value66,Value67,Value68,Value69,Value70,Value71,Value72,Value73,Value74,Value75,Value76,Value77,Value78,Value79,Value80,Value81,Value82,Value83,Value84,Value85,Value86,Value87,Value88,Value89,Value90,Value91,Value92,Value93,Value94,Value95,Value96,Value97,Value98,Value99,Value00',
            '"100000","World","117100","South Africa",1137424,1253225,1315703,1453614,1719904,1934726,2073399,2172388,2067276,2087840,2197399,3035278,4473097,5151976,5786599,7168917,8039418,10691282,12774748,31497500,9593869,8498300,27745267,11587906,12944273,12142881,14767609,15973854,16353354,16153549,30129310,27374820,30949042,33215626,28668008,35065432,30622443,31679773,38330367',
            '"100000","World","100000","World",130820766,144752269,163401432,178619568,196373987,206306598,229438483,261773445,301725595,336632436,394429429,547697681,822593098,860894299,967082574,1080137888,1187499282,1588616996,1927615343,1908925277,1753041348,1650817500,1875030686,1949413915.813,2097956459,2454677596,2798583134,3044659532,3471060661,3600841444,3860180402,3796916610,4305600574,5136222078,5475815227,5631902195,5575802767,5791258924,6568385296',
            '"218400","USA","117100","South Africa",251562,254890,2545490,225124,250540,228294,255674,247306,290816,287973,NaN,NaN,657842,926241,1013444,1336176,2538904,2798597,3562230,2754026,2120687,2157953,2651509,2218343,2503722,1436099,1633206,1664480,1861072,1879078,1906935,2037416,2274562,2438873,2586155,2838329,3389674,3530854,4646342',
            '"220600","Bermuda","141400","Cent.Afr.Rep",116,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN')
        d = ExportData()
        d.load_file(f.name, should_read_world_datapoints=True)
        self.assertEquals(65948856, d.total_exports_from_C1_to_C2('South Africa', 'USA'))
        self.assertEquals(36, d.total_non_nan_points_from_C1_to_C2('South Africa', 'USA'))
        self.assertEquals(0, d.total_non_nan_points_from_C1_to_C2('Cent.Afr.Rep', 'Bermuda'))
    #        this test should pass?
#        self.assertEquals(0, d.total_non_nan_points_from_C1_to_C2('Bermuda', 'Cent.Afr.Rep'))


