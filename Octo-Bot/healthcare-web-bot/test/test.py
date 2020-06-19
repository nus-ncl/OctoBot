import unittest
import warnings
import io
import sys
from testUtil.testDriver.daemon import daemonMode
from testUtil.testDriver.adminparser import getUrl, getNumberRecords
from testUtil.testDriver.patientparser import patientGetNumberRecords
from testUtil.testDriver.therapistparser import therapistGetNumberRecords
from testmain import getDriver

url = "https://10.10.0.112"

class Testing(unittest.TestCase):

    """
    Test functions to check if the bot is running properly
    getUrl checks if the valid url is used
    testAdminCSV tests if the number of records in the admin.csv files tally
    testPatientCSV tests if the number of records in the patient.csv files tally
    testTherapistCSV tests if the number of records in the therapist.csv files tally
    testDaemon tests if the daemon mode is running properly
    """
    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)
        warnings.simplefilter('ignore', category = ResourceWarning)
        
    def testUrl(self):
        adminUrl = getUrl()
        self.assertEqual(url, adminUrl)

    def testAdminCSV(self):
        number = getNumberRecords()
        self.assertEqual(number, 790)
    
    def testPatientCSV(self):
        number = patientGetNumberRecords()
        self.assertEqual(number, 102)
    
    def testTherapistCSV(self):
        number = therapistGetNumberRecords()
        self.assertEqual(number, 123)
    
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
