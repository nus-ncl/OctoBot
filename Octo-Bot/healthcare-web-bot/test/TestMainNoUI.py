import argparse
import os
import random
import time

from selenium import webdriver

from TestUtil.TestDriver.adminparser import (checkFilesExist, genAdminFiles,
                                             getCredentials, getUrl, writeBack)
from TestUtil.TestDriver.daemon import daemonMode
from TestUtil.TestDriver.login import login, logout
from TestUtil.TestDriver.patientparser import (genPatientFiles,
                                               patientCheckFilesExist,
                                               patientGetCredentials,
                                               patientGetNumberRecords,
                                               patientWriteBack)
from TestUtil.TestDriver.role import isAdmin, isPatient, isTherapist
from TestUtil.TestDriver.therapistparser import (genTherapistFiles,
                                                 therapistCheckFilesExist,
                                                 therapistGetCredentials,
                                                 therapistGetNumberRecords,
                                                 therapistWriteBack)
from TestUtil.TestScrapeAdmin.accountlogs import getAllAccountLogs
from TestUtil.TestScrapeAdmin.contact import getAllContactInformation
from TestUtil.TestScrapeAdmin.NRIC import getAllNric
from TestUtil.TestScrapeAdmin.patient import getAllPatientInformation
from TestUtil.TestScrapeAdmin.permissionslogs import getAllPermissionLogs
from TestUtil.TestScrapeAdmin.personal import getAllPersonalInformation
from TestUtil.TestScrapeAdmin.recordlogs import getAllRecordLogs
from TestUtil.TestScrapeAdmin.researcher import getAllResearcherInformation
from TestUtil.TestScrapeAdmin.status import getAllStatusInformation
from TestUtil.TestScrapeAdmin.therapist import getAllTherapistInformation
from TestUtil.TestScrapePatient.newrecord import createNewRecords
from TestUtil.TestScrapePatient.viewDiagnosis import getDiagnosisInformation
from TestUtil.TestScrapePatient.viewTherapist import getTherapistInformation
from TestUtil.TestScrapeTherapist.viewPatients import (iteratePage,
                                                       loginTherapist)

headerUrl = "https://10.10.0.112/"

def getDriver(username, password, url):
    
    '''
    Obtains the driver to be used to start the firefox instance

    Arguments:
        username(str) : Username of credentials that the driver is logging in to
        password(str) : password of credentials that the driver is logging in to
        url(str) : url of the website that the driver is accessing
    
    Returns:
        driver object
    '''
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

def adminActions(driver, sleepTime, headerUrl):

    '''
    Main Logic behind all the actions carried out by the admin role

    Arguments:
        driver(obj): firefox webdriver instance in python 
        sleepTime(int) : The sleeptime between each admin actions defined by the user
    
    Returns:
        None
    '''
    getAllNric(driver, headerUrl)
    time.sleep(sleepTime)
    getAllPersonalInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllContactInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllTherapistInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllResearcherInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllStatusInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllPatientInformation(driver, headerUrl)
    time.sleep(sleepTime)
    getAllAccountLogs(driver, headerUrl)
    time.sleep(sleepTime)
    getAllRecordLogs(driver, headerUrl)
    time.sleep(sleepTime)
    getAllPermissionLogs(driver, headerUrl)
    time.sleep(sleepTime)
    createNewRecords(driver, headerUrl)

def therapistRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl):

    '''
    Main Logic behind all the therapist actions

    Arguments:
        checkUsername(str) : Username that the bot is going to log in with
        checkPassword(str) : password that the bot is going to log in with
        sleepTime(int) : sleep time between each therapist actions taken by the bot
        botNumbers(int) : Number of consecutive therapist bots running at the same time
    
    Returns:
        None
    '''
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
    if driver.current_url == headerUrl + "Therapist/Dashboard":
        print("Logged in as a single-role therapist...")
        iteratePage(driver, username)
        time.sleep(sleepTime)
    else:
        print("Trying to login multi-role therapist..")
        if isTherapist(driver):
            loginTherapist(driver, headerUrl)
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

        
def adminRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl):

    '''
    Main logic behind the actins taken by an admin bot

    Arguments:
        checkUsername(str) : Username that the bot is going to login with
        checkPassword(str) : Password that the bot is going to login with
        url(str) : Url that the bot is going to login with
        sleepTime(int) : Sleep time between each admin actions as defined by the user
        botNumbers(int) : Number of admin bots running consecutively
    
    Returns:
        None
    '''
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
        adminActions(driver, sleepTime, headerUrl)
    else:
        print("Invalid role found!")
    logout(driver)
    writeBack(username, password, fileNumber)
    driver.close()
    driver.quit()

def patientRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl):

    '''
    Main logic behind the actins taken by a patient bot
    
    Arguments:
        checkUsername(str) : Username that the bot is going to login with
        checkPassword(str) : Password that the bot is going to login with
        url(str) : Url that the bot is going to login with
        sleepTime(int) : Sleep time between each patient actions as defined by the user
        botNumbers(int) : Number of patient bots running consecutively
    
    Returns:
        None
    '''
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
        getDiagnosisInformation(driver, username, headerUrl)
        getTherapistInformation(driver, username, headerUrl)
        time.sleep(sleepTime)
    else:
        print("Trying to login multi-role patient..")
        if isPatient(driver):
            driver.find_element_by_id('BodyContent_buttonLoginPatient').click()
            time.sleep(sleepTime)
            print("Running patient role...")
            getDiagnosisInformation(driver, username, headerUrl)
            getTherapistInformation(driver, username, headerUrl)
            time.sleep(sleepTime)
        else:
            print("Invalid Role found!!")
    logout(driver)
    patientWriteBack(username, password, fileNumber)
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
        help='Number of credentials for the choosen role', default = 1)
    parser.add_argument('-u', metavar = 'username', type=str, \
        help='Username to be used for login', default = '')
    parser.add_argument('-p', metavar = 'password', type=str, \
        help='Password to be used for login', default = '')
    parser.add_argument('-m', metavar = 'mode of execution', type=str, \
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
        try:
            if role.lower() == "admin":
                adminRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl)
                print("Website scraping completed!")
            elif role.lower() == "therapist":
                therapistRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl)
                print("Website scraping completed")
            elif role.lower() == "patient":
                patientRun(checkUsername, checkPassword, url, sleepTime, botNumbers, headerUrl)
                print("Website scraping completed")
            else:
                print("No such roles found")
        except:
            print("Error in csv file. Please check again!")
