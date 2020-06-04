
import unittest
import warnings
import io
import sys
from testUtil.testDriver.testParser import *
from testMain import getDriver

class Testing(unittest.TestCase):

    currentResult = None

    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)
    
    # tearDown and run functions was referenced from https://stackoverflow.com/questions/4414234/getting-pythons-unittest-results-in-a-teardown-method
    def tearDown(self):
        ok = self.currentResult.wasSuccessful()
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        if ok:
            print("All tests passed so far!")
        else:
            print("%d errors and %d failures", len(errors), len(failures))
    
    def run(self, result=None):
        self.currentResult = result
        unittest.TestCase.run(self, result) 
    def testUrl(self):
        url = str(getUrl())
        actualUrl = "http://10.10.0.112"
        self.assertEqual(url, actualUrl)
    
    def testDriver(self):
        username = "S1234567B"
        password = "easyP@ssw0rd"
        url = "http://10.10.0.112"
        driver = getDriver(username, password, url)
        self.assertIsNotNone(driver)
    
    def testLogin(self):
        isLoggedIn = False
        username = "S1234567B"
        password = "easyP@ssw0rd"
        url = "http://10.10.0.112"
        out = io.StringIO()
        sys.stdout = out
        driver = getDriver(username, password, url)
        sys.stdout = sys.__stdout__
        if "Logged in" in out.getvalue():
            isLoggedIn = True
        self.assertTrue(isLoggedIn)

if __name__ == '__main__':
    unittest.main()
