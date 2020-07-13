import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

def saveStatusInformation(driver, researcherToken, directory):
    
    '''
    Main logic to save status information
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        researcherToken(str) : Token to get the xpath for pagination
        directory(str) : Directory to store status information
    
    Returns:
        None
    '''
    print("Printing status information...")
    time.sleep(3)
    driver.find_element_by_xpath(researcherToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_labelStatusNRIC").text)
    outDirectory = directory + "/data/admin/" + nric + ".txt"
    savedFile = open(outDirectory,"a")
    patientPermissions = str(driver.find_element_by_id('BodyContent_LabelRolePatient').text)
    therapistPermissions = str(driver.find_element_by_id('BodyContent_LabelRoleTherapist').text)
    researcherPermissions = str(driver.find_element_by_id('BodyContent_LabelRoleResearcher').text)
    adminPermissions = str(driver.find_element_by_id('BodyContent_LabelRoleAdmin').text)
    registrationDate = str(driver.find_element_by_id('BodyContent_inputStatusCreateTime').get_attribute('value'))
    lastLogin = str(driver.find_element_by_id('BodyContent_inputStatusLastLogin').get_attribute('value'))
    mfaToken = str(driver.find_element_by_id('BodyContent_TextboxMFATokenIDUpdate').get_attribute('value'))
    mfaDevice = str(driver.find_element_by_id('BodyContent_TextboxMFADeviceIDUpdate').get_attribute('value'))
    if registrationDate == "":
        registrationDate = "NIL"
    if lastLogin == "":
        lastLogin = "NIL"
    if mfaToken == "":
        mfaToken = "NIL"
    if mfaDevice == "":
        mfaDevice = "NIL"
    savedFile.write("Registration date: " + registrationDate + "\n")
    savedFile.write("Last Login: " + lastLogin + "\n")
    savedFile.write("MFA Token id: " + mfaToken + "\n")
    savedFile.write("MFA Device id: " + mfaDevice + "\n")
    savedFile.write("Permissions:\n")
    savedFile.write("Patient Permissions: " + patientPermissions + "\n")
    savedFile.write("Therapist permissions: " + therapistPermissions + "\n")
    savedFile.write("Researcher permissions: " + researcherPermissions + "\n")
    savedFile.write("Adminstrator permissions" + adminPermissions + "\n")
    savedFile.close()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getStatusInformationOnePage(driver, directory):

    '''
    Obtains status information in a single webpage

    Arguments:
        driver(obj): firefox webdriver instance in python
        directory(str) : Directory to store status information
    
    Returns:
        None
    '''
    number = 2
    while (number <= 6):
        statusToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[7]/a"
        saveStatusInformation(driver, statusToken, directory)
        number +=1

def getAllStatusInformation(driver, headerUrl):

    '''
    Obtains all the status information from all the webpages

    Arguments:
        driver(obj): firefox webdriver instance in python    
    
    Returns:
        None
    '''
    driver.get(headerUrl + "Admin/Manage-Accounts/View")
    maxNumber = viewAccountPages(driver)
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            getStatusInformationOnePage(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getStatusInformationOnePage(driver, directory)
