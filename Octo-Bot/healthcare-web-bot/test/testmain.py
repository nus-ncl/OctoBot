import argparse
import os
import random
import time

from selenium import webdriver

from testUtil.testDriver.testadminparser import (
    checkFilesExist, genAdminFiles, getCredentials, getUrl, writeBack)
from testUtil.testDriver.testdaemon import daemonMode
from testUtil.testDriver.testlogin import login, logout
from testUtil.testDriver.testpatientparser import (genPatientFiles,
                                                   patientCheckFilesExist,
                                                   patientGetCredentials,
                                                   patientGetNumberRecords,
                                                   patientWriteBack)
from testUtil.testDriver.testrole import isAdmin, isPatient, isTherapist
from testUtil.testDriver.testtherapistparser import (
    genTherapistFiles, therapistCheckFilesExist, therapistGetCredentials,
    therapistGetNumberRecords, therapistWriteBack)
from testUtil.testScrapeAdmin.testaccountlogs import getAllAccountLogs
from testUtil.testScrapeAdmin.testcontact import getAllContactInformation
from testUtil.testScrapeAdmin.testNRIC import getAllNric
from testUtil.testScrapeAdmin.testpatient import getAllPatientInformation
from testUtil.testScrapeAdmin.testpermissionslogs import getAllPermissionLogs
from testUtil.testScrapeAdmin.testpersonal import getAllPersonalInformation
from testUtil.testScrapeAdmin.testrecordlogs import getAllRecordLogs
from testUtil.testScrapeAdmin.testresearcher import getAllResearcherInformation
from testUtil.testScrapeAdmin.teststatus import getAllStatusInformation
from testUtil.testScrapeAdmin.testtherapist import getAllTherapistInformation
from testUtil.testScrapePatient.testnewrecord import createNewRecords
from testUtil.testScrapePatient.testviewdiagnosis import \
    getDiagnosisInformation
from testUtil.testScrapePatient.testviewtherapist import \
    getTherapistInformation
from testUtil.testScrapeTherapist.testviewpatients import (iteratePage,
                                                           loginTherapist)


def getDriver(username, password, url):
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    # firefox_options.add_argument("--no-sandbox")
    # firefox_options.add_argument("--disable-dev-shm-usage")
    # firefox_options.add_argument("--disable-gpu")
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

def therapistRun(checkUsername, checkPassword, url, sleepTime, botNumbers):
    if (checkUsername == '' or checkPassword == ''):
        if (therapistCheckFilesExist(botNumbers) == False):
            genTherapistFiles(botNumbers)
        credentials = therapistGetCredentials(botNumbers)
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
    driver = getDriver(username, password, url)
    if driver.current_url == "https://10.10.0.112/Therapist/Dashboard":
        print("Logged in as a single-role therapist...")
        iteratePage(driver, username)
        time.sleep(sleepTime)
    else:
        print("Trying to login multi-role therapist..")
        if isTherapist(driver):
            loginTherapist(driver)
            time.sleep(sleepTime)
            print("Running therapist role...")
            iteratePage(driver, username)
            time.sleep(sleepTime)
        else:
            print("Invalid Role found!!")
    logout(driver)
    therapistWriteBack(username, password, fileNumber)
    driver.close()
    driver.quit()

        
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

def patientRun(checkUsername, checkPassword, url, sleepTime, botNumbers):
    if (checkUsername == '' or checkPassword == ''):
        if (patientCheckFilesExist(botNumbers) == False):
            genPatientFiles(botNumbers)
        credentials = patientGetCredentials(botNumbers)
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
    if driver.current_url == "https://10.10.0.112/Patient/Dashboard":
        print("Logged in as a single-role patient...")
        getDiagnosisInformation(driver, username)
        getTherapistInformation(driver, username)
        time.sleep(sleepTime)
    else:
        print("Trying to login multi-role patient..")
        if isPatient(driver):
            driver.find_element_by_id('BodyContent_buttonLoginPatient').click()
            time.sleep(sleepTime)
            print("Running patient role...")
            getDiagnosisInformation(driver, username)
            getTherapistInformation(driver, username)
            time.sleep(sleepTime)
        else:
            print("Invalid Role found!!")
    logout(driver)
    patientWriteBack(username, password, fileNumber)
    driver.close()
    driver.quit()
    # username = checkUsername
    # password = checkPassword
    # driver = getDriver(username, password, url)
    # getDiagnosisInformation(driver, username)
    # getTherapistInformation(driver, username)
    # print(driver.current_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = \
        "Arguments for program")
    parser.add_argument('-t', metavar = 'time', type=int, \
        help='Time to sleep between crawling of website links', default = 0)
    parser.add_argument('-r', metavar = 'role', type=str, \
        help='Role that the bot should login as', default = "admin")
    parser.add_argument('-b', metavar = 'bot', type=int, \
        help='Number of credentials for the choosen role', default = 1)
    parser.add_argument('-u', metavar = 'username', type=str, \
        help='Username to be used for login', default = '')
    parser.add_argument('-p', metavar = 'password', type=str, \
        help='Password to be used for login', default = '')
    parser.add_argument('-m', metavar = 'modeof execution', type=str, \
        help='Mode for bot to be executed', default = '')

    args = parser.parse_args()
    sleepTime = args.t
    role = args.r
    botNumbers = args.b
    mode = args.m
    number = random.randint(sleepTime,2000)%17
    time.sleep(number)
    url = getUrl()
    number = random.randint(sleepTime,1345) % 13
    time.sleep(number)
    checkUsername = str(args.u)
    checkPassword = str(args.p)
    if mode.lower() == "daemon":
        daemonMode()
    else:
        print("Preparing to scrap website...")
        if role.lower() == "admin":
            adminRun(checkUsername, checkPassword, url, sleepTime, botNumbers)
            print("Website scraping completed!")
        elif role.lower() == "therapist":
            therapistRun(checkUsername, checkPassword, url, sleepTime, botNumbers)
            print("Website scraping completed")
        elif role.lower() == "patient":
            patientRun(checkUsername, checkPassword, url, sleepTime, botNumbers)
            print("Website scraping completed")
        else:
            print("No such roles found")
