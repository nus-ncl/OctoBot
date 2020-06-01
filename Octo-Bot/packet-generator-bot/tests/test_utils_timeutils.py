import unittest

from utils.TimeUtils import *

class TestTimeUtilsMethods(unittest.TestCase):
    '''
    Unit tests to ensure the time utils functions work as expected.
    If any tests fail, please check for regression.

    Expected output:
        ....
        ----------------------------------------------------------------------
        Ran 10 tests in X.XXXs

        OK
    '''

    def test_timeStr2Secs_JustSeconds(self):
        timeStr = "123456"
        self.assertEqual(timeStr2Secs(timeStr), 123456)
    
    def test_timeStr2Secs_Seconds(self):
        timeStr = "00:00:00:18"
        self.assertEqual(timeStr2Secs(timeStr), 18)
    
    def test_timeStr2Secs_Minutes(self):
        timeStr = "00:00:19:00"
        self.assertEqual(timeStr2Secs(timeStr), 1140)

    def test_timeStr2Secs_Hours(self):
        timeStr = "00:20:00:00"
        self.assertEqual(timeStr2Secs(timeStr), 72000)
    
    def test_timeStr2Secs_Days(self):
        timeStr = "21:00:00:00"
        self.assertEqual(timeStr2Secs(timeStr), 1814400)

    def test_timeStr2Secs_MinutesAndSeconds(self):
        timeStr = "1:2"
        self.assertEqual(timeStr2Secs(timeStr), 62)
    
    def test_timeStr2Secs_HoursAndMinutesAndSeconds(self):
        timeStr = "1:2:3"
        self.assertEqual(timeStr2Secs(timeStr), 3723)

    def test_timeStr2Secs_DaysAndHoursAndMinutesAndSeconds(self):
        timeStr = "1:2:3:4"
        self.assertEqual(timeStr2Secs(timeStr), 93784)

    def test_timeStr2Secs_NegativeMinutes(self):
        timeStr = "-1:00"
        self.assertEqual(timeStr2Secs(timeStr), 0)
    
    def test_timeStr2Secs_Blank(self):
        timeStr = ""
        self.assertEqual(timeStr2Secs(timeStr), 0)

        
if __name__ == '__main__':
    unittest.main()