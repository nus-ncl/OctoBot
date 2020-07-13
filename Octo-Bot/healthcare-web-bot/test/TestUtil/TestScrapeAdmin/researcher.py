import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

def saveResearcherInformation(driver, researcherToken, directory):

    '''
    Main logic to save researcher information
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        researcherToken(str) : Token for the driver to find the xpath for researcher
        directory(str) : Directory to save the researcher information
    
    Returns:
        None
    '''
    print("Printing researcher information...")
    time.sleep(3)
    driver.find_element_by_xpath(researcherToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_labelResearcherNRIC").text)
    jobTitle = str(driver.find_element_by_id('BodyContent_inputResearcherJobTitle').get_attribute('value'))
    department = str(driver.find_element_by_id('BodyContent_inputResearcherDepartment').get_attribute('value'))
    if jobTitle == "":
        jobTitle = "NIL"
    if department == "":
        department = "NIL"
    outDirectory = directory + "/data/admin/" + str(nric) + ".txt"
    savedFile = open(outDirectory, "a")
    savedFile.write("Researcher Information\n")
    savedFile.write("Job Title: " + jobTitle + "\n")
    savedFile.write("Department: " + department + "\n")
    savedFile.close()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getResearcherInformationOnePage(driver, directory):
    
    '''
    Obtains researcher information from 1 webpage
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        directory(str) : Directory to save researcher information
    
    Returns:
        None
    '''
    number = 2
    while (number <= 6):
        therapistToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[6]/a"
        saveResearcherInformation(driver, therapistToken, directory)
        number +=1

def getAllResearcherInformation(driver, headerUrl):

    '''
    Obtains all the researcher information

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        None
    '''
    driver.get(headerUrl + "Admin/Manage-Accounts/View")
    time.sleep(3)
    maxNumber = viewAccountPages(driver)
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            getResearcherInformationOnePage(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                 break
            number += 1
            driver.get(headerUrl + "Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getResearcherInformationOnePage(driver, directory)
