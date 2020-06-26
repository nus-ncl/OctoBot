import unittest
import warnings
import io
import sys
from FileParser import getAdminCredentials, getTherapistCredentials, getPatientCredentials
from BotActions import getDriver

class Testing(unittest.TestCase):
    '''
    Unit tests to test that csv files can be read and driver operates as expected
    If any tests fail, please check for regression

    Expected output:
        ....
        ----------------------------------------------------------------------
        Ran 4 tests in X.XXXs
        OK        
    '''
    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)
        warnings.simplefilter('ignore', category = ResourceWarning)
    
    def testGetAdminCredentials(self):
        adminCredentials = getAdminCredentials()
        adminCredentialsData = ["S0000001A", "DrasticP@ssw0rdPlayer"]
        self.assertEqual(adminCredentials, adminCredentialsData)
    
    def testGetTherapistCredentials(self):
        therapistCredentials = getTherapistCredentials()
        therapistCredentialsData = ["F0058132Q", "LightEnterP@ssw0rd", "Z9989"]
        self.assertEqual(therapistCredentials, therapistCredentialsData)
    
    def testGetPatientCredentials(self):
        patientCredentials = getPatientCredentials()
        patientCredentialsData = ["S1757946A", "1995-12-12", "John", "Tan", "Block 5002 Ang Mo Kio Avenue 5 04-05 TECHplace II Singapore 569871  Singapore", "john@email.com", "569871", "12345678", "veryEasyP@ssw0rd", "Weight", "20"]
        self.assertEqual(patientCredentials, patientCredentialsData)

    def testGetDriver(self):
        url = "https://10.10.0.112/"
        driver = getDriver(url)
        self.assertIsNotNone(driver)
        
if __name__ == '__main__':
    unittest.main()
