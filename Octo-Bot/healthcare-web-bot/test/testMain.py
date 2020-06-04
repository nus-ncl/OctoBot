import time

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

from testUtil.testDriver.testLogin import login, logout
from testUtil.testDriver.testParser import getUrl, getCredentials
from testUtil.testScrapeAdmin.testAccountLogs import getAllAccountLogs
from testUtil.testScrapeAdmin.testContact import getAllContactInformation
from testUtil.testScrapeAdmin.testNRIC import getAllNric
from testUtil.testScrapeAdmin.testPatient import getAllPatientInformation
from testUtil.testScrapeAdmin.testPermissionsLogs import getAllPermissionLogs
from testUtil.testScrapeAdmin.testPersonal import getAllPersonalInformation
from testUtil.testScrapeAdmin.testRecordLogs import getAllRecordLogs
from testUtil.testScrapeAdmin.testResearcher import getAllResearcherInformation
from testUtil.testScrapeAdmin.testStatus import getAllStatusInformation
from testUtil.testScrapeAdmin.testTherapist import getAllTherapistInformation
from testUtil.testScrapePatient.testNewRecord import createNewRecords
from testUtil.testDriver.testRole import isAdmin
import os
import random

path = str(os.getcwd()) + "/testUtil/resources/drivers/geckodriver.exe"
def getDriver(username, password, url):
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(firefox_options = firefox_options,firefox_profile = profile)
    driver.get(url)
    login(driver, username, password)
    return driver

def driverRun(username, password, url, func):
    driver = getDriver(username, password, url)
    func(driver)
    logout(driver)
    time.sleep(10)
    driver.close()
    driver.quit()

def run(username, password, url):
    driver = getDriver(username,password,url)
    if isAdmin(driver):
        getAllNric(driver)
        time.sleep(3)
        getAllPersonalInformation(driver)
        time.sleep(3)
        getAllContactInformation(driver)
        time.sleep(3)
        getAllTherapistInformation(driver)
        time.sleep(3)
        getAllResearcherInformation(driver)
        time.sleep(3)
        getAllStatusInformation(driver)
        time.sleep(3)
        getAllPatientInformation(driver)
        time.sleep(3)
        getAllAccountLogs(driver)
        time.sleep(3)
        getAllRecordLogs(driver)
        time.sleep(3)
        getAllPermissionLogs(driver)
        time.sleep(3)
        createNewRecords(driver)
    logout(driver)
    driver.close()
    driver.quit()

def patientRun(username, password, url):
    print("Preparing to create new patient records...")
    driverRun(username, password, url, createNewRecords)

if __name__ == "__main__":
    number = random.randint(1,2000)%17
    time.sleep(number)
    url = getUrl()
    number = random.randint(1,1345) % 13
    time.sleep(number)
    credentials = getCredentials()
    username = credentials[0]
    password = credentials[1]
    print("Username used: " + str(username))
    print("Password used: " + str(password))
    print("Preparing to scrap website...")
    run(username, password, url)
    print("Website scraping completed!")
