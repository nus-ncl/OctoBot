import unittest
from util.Driver.parser import *
from main import getDriver

class Testing(unittest.TestCase):
    
    def testUrl(self):
        url = str(getUrl())
        actualUrl = "http://10.10.0.112"
        self.assertEqual(url, actualUrl)
        
if __name__ == '__main__':
    unittest.main()