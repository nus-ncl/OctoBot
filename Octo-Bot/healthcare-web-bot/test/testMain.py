import time

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

from util.Driver.login import login, logout
from util.Driver.parser import getUrl, getCredentials
from util.ScrapeAdmin.accountlogs import getAllAccountLogs
from util.ScrapeAdmin.contact import getAllContactInformation
from util.ScrapeAdmin.NRIC import getAllNric
from util.ScrapeAdmin.patient import getAllPatientInformation
from util.ScrapeAdmin.permissionslogs import getAllPermissionLogs
from util.ScrapeAdmin.personal import getAllPersonalInformation
from util.ScrapeAdmin.recordlogs import getAllRecordLogs
from util.ScrapeAdmin.researcher import getAllResearcherInformation
from util.ScrapeAdmin.status import getAllStatusInformation
from util.ScrapeAdmin.therapist import getAllTherapistInformation
from util.ScrapePatient.newrecord import createNewRecords
from util.Driver.role import isAdmin
import os
import random

path = str(os.getcwd()) + "/util/resources/drivers/geckodriver.exe"
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
