import unittest

from scapy.all import *

from helper.ReplayHelper import *


class TestReplayHelperMethods(unittest.TestCase):
    '''
    Unit tests to ensure the replay helper functions work as expected. 
    If any tests fail, please check for regression.

    Expected output:
        ....
        ----------------------------------------------------------------------
        Ran 4 tests in X.XXXs

        OK
    '''

    def test_openCorrect(self):
        self.assertIsNotNone(openPcap("captures/http.cap"))
    
    def test_openWrong(self):
        self.assertIsNone(openPcap("this/file/does/not/exist"))
    
    def test_openInt(self):
        self.assertIsNone(openPcap(777))
    
    def test_openList(self):
        with self.assertRaises(TypeError):
            openPcap(['should', 'not', 'work'])
        
if __name__ == '__main__':
    unittest.main()