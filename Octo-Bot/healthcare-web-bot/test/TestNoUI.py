import unittest
import warnings
import io
import sys
from TestUtil.TestDriver.daemon import daemonMode
from TestUtil.TestDriver.adminparser import getUrl, getNumberRecords
from TestUtil.TestDriver.patientparser import patientGetNumberRecords
from TestUtil.TestDriver.therapistparser import therapistGetNumberRecords
from TestMainNoUI import getDriver

url = "https://10.10.0.112"

class Testing(unittest.TestCase):

    '''
    Unit tests to test that healthcare-wb-bot is functioning properly without Firefox web interface UI

    Expected output:
        ......
        ----------------------------------------------------------------------
        Ran 6 tests in X.XXXs
        OK        
    ''' 
    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)
        warnings.simplefilter('ignore', category = ResourceWarning)
        text_trap = io.StringIO()
        sys.stdout = text_trap
        
    def testUrl(self):
        adminUrl = getUrl()
        self.assertEqual(url, adminUrl)

    def testAdminCSV(self):
        error = None
        try:
            number = getNumberRecords()
        except Exception as e:
            error = e
        self.assertIsNone(error)

    def testPatientCSV(self):
        error = None
        try:
            number = patientGetNumberRecords()
        except Exception as e:
            error = e
        self.assertIsNone(error)

    def testTherapistCSV(self):
        error = None
        try:
            number = therapistGetNumberRecords()
        except Exception as e:
            error = e
        self.assertIsNone(error)
    
    def testDriver(self):
        username = "S1234567B"
        password = "easyP@ssw0rd"
        driver = getDriver(username, password, url)
        driver.close()
        driver.quit()
        self.assertIsNotNone(driver)
        
    def testDaemon(self):
        isDaemonMode = True
        out = io.StringIO()
        sys.stdout = out
        daemonMode
        sys.stdout = sys.__stdout__
        if "Finishing of thread" in out.getvalue():
            isDaemonMode = False
        self.assertTrue(isDaemonMode)


if __name__ == '__main__':
    unittest.main()
