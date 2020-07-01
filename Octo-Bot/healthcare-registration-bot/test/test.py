import io
import sys
import unittest
import warnings

from BotActions import (adminLogin, assignTherapist, getDriver,
                        getDriverStatus, registerPatientAccount)
from FileParser import (getAdminCredentials, getPatientCredentials,
                        getTherapistCredentials)
from main import main


class Testing(unittest.TestCase):
    '''
    Unit tests to test that csv files can be read and driver operates as expected
    If any tests fail, please check for regression

    Expected output:
        ......
        ----------------------------------------------------------------------
        Ran 7 tests in X.XXXs
        OK        
    ''' 
    def setUp(self):
        warnings.simplefilter('ignore',category = DeprecationWarning)
        warnings.simplefilter('ignore', category = ResourceWarning)
        text_trap = io.StringIO()
        sys.stdout = text_trap

    def testGetAdminCredentials(self):
        adminCredentials = getAdminCredentials()
        adminCredentialsData = ["S1234567C", "easyP@ssw0rd"]
        self.assertEqual(adminCredentials, adminCredentialsData)
    
    def testGetTherapistCredentials(self):
        therapistCredentials = getTherapistCredentials()
        therapistCredentialsData = ["S1234567D", "easyP@ssw0rd", "Z9989"]
        self.assertEqual(therapistCredentials, therapistCredentialsData)
    
    def testGetPatientCredentials(self):
        patientCredentials = getPatientCredentials()
        patientCredentialsData = ["S1757946A", "1995-12-12", "John", "Tan", "Block 5002 Ang Mo Kio Avenue 5 04-05 TECHplace II Singapore 569871  Singapore", "john@email.com", "569871", "12345678", "veryEasyP@ssw0rd", "Weight", "20"]
        self.assertEqual(patientCredentials, patientCredentialsData)

    def testGetDriver(self):
        url = "https://10.10.0.112/"
        driver = getDriver(url)
        driver.close()
        driver.quit()
        self.assertIsNotNone(driver)
    
    def testGetDriverStatus(self):
        url = "https://10.10.0.112/"
        driver = getDriver(url)
        driverStatus = getDriverStatus(driver)
        self.assertEqual(driverStatus, "alive")
        driver.close()
        driver.quit()
        driverStatus = getDriverStatus(driver)
        self.assertEqual(driverStatus, "dead")
    
    def testAdminActions(self):
        url = "https://10.10.0.112/"
        adminCredentials = getAdminCredentials()
        error = None
        try:
            driver = getDriver(url)
            adminLogin(url, driver, adminCredentials[0], adminCredentials[1])
            registerPatientAccount(url, driver)
            assignTherapist(url, driver)
        except Exception as e:
            error = e
        self.assertIsNone(error)
    
    def testMain(self):
        error = False
        url = "https://10.10.0.112/"
        try:
            main(url)
        except Exception as e:
            print(e)
            error = True
        self.assertFalse(error)

if __name__ == '__main__':
    unittest.main()
