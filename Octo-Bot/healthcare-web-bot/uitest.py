
import unittest
import warnings
import io
import sys
from util.Driver.parser import *
from test import getDriver


def test():
    username = "S1234567B"
    password = "easyP@ssw0rd"
    url = "http://10.10.0.112"
    out = io.StringIO()
    sys.stdout = out
    driver = getDriver(username, password, url)
    sys.stdout = sys.__stdout__
    print(out.getvalue())

class Testing(unittest.TestCase):

    test_failed = False

    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)

    def teardown(self):
        super(Testing, self).teardown()
        print(self.test_failed)

    # def test_string(self):
    #     a = 'some'
    #     b = 'some'
    #     self.assertEqual(a, b)

    # def test_boolean(self):
    #     a = True
    #     b = True
    #     self.assertEqual(a, b)
    
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
    # test()
