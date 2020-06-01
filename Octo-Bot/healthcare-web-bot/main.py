import argparse
import os
import random
import time

from selenium import webdriver

from util.Driver.login import login, logout
from util.Driver.parser import getUrl, genAdminFiles, getCredentials, writeBack, checkFilesExist
from util.Driver.role import isAdmin
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

def adminActions(driver, sleepTime):
    getAllNric(driver)
    time.sleep(sleepTime)
    getAllPersonalInformation(driver)
    time.sleep(sleepTime)
    getAllContactInformation(driver)
    time.sleep(sleepTime)
    getAllTherapistInformation(driver)
    time.sleep(sleepTime)
    getAllResearcherInformation(driver)
    time.sleep(sleepTime)
    getAllStatusInformation(driver)
    time.sleep(sleepTime)
    getAllPatientInformation(driver)
    time.sleep(sleepTime)
    getAllAccountLogs(driver)
    time.sleep(sleepTime)
    getAllRecordLogs(driver)
    time.sleep(sleepTime)
    getAllPermissionLogs(driver)
    time.sleep(sleepTime)
    createNewRecords(driver)

def adminRun(checkUsername, checkPassword, url, sleepTime, botNumbers):
    if (checkUsername == '' or checkPassword == ''):
        if (checkFilesExist(botNumbers) == False):
            genAdminFiles(botNumbers)
        credentials = getCredentials(botNumbers)
        username = credentials[0]
        password = credentials[1]
        fileNumber = credentials[2]
    else:
        fileNumber = "No files are used"
        username = checkUsername
        password = checkPassword
    print("Username used: " + str(username))
    print("Password used: " + str(password))
    print("File Number used: " + str(fileNumber))
    driver = getDriver(username,password,url)
    if isAdmin(driver):
        print("Running admin role...")
        adminActions(driver, sleepTime)
    else:
        print("Invalid role found!")
    logout(driver)
    writeBack(username, password, fileNumber)
    driver.close()
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = \
        "Arguments for program")
    parser.add_argument('-t', metavar = 'time', type=int, \
        help='Time to sleep between crawling of website links', default = 0)
    parser.add_argument('-r', metavar = 'role', type=str, \
        help='Role that the bot should login as', default = "admin")
    parser.add_argument('-b', metavar = 'bot', type=int, \
        help='Number of bots for the choosen role', default = 1)
    parser.add_argument('-u', metavar = 'username', type=str, \
        help='Username to be used for login', default = '')
    parser.add_argument('-p', metavar = 'password', type=str, \
        help='Password to be used for login', default = '')
    args = parser.parse_args()
    sleepTime = args.t
    role = args.r
    botNumbers = args.b
    number = random.randint(sleepTime,2000)%17
    time.sleep(number)
    url = getUrl()
    number = random.randint(sleepTime,1345) % 13
    time.sleep(number)
    checkUsername = str(args.u)
    checkPassword = str(args.p)
    print("Preparing to scrap website...")
    if role.lower() == "admin":
        adminRun(checkUsername, checkPassword, url, sleepTime, botNumbers)
        print("Website scraping completed!")
    else:
        print("No such roles found")
