import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

def saveTherapistInformation(driver, therapistToken, directory):
    
    '''
    Main Logic to obtain all the therapist information
    
    Arguments:
        driver(obj): firefox webdriver instance in python  
        therapistToken(str) : token for driver to get xpath for pagination for therapist role
        directory(str) : directory for saving therapist information
    
    Returns:
        None
    '''
    print("Printing therapist information...")
    time.sleep(3)
    driver.find_element_by_xpath(therapistToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_labelTherapistNRIC").text)
    outDirectory = directory + "/data/admin/" + str(nric) + ".txt"
    savedFile = open(outDirectory, "a")
    jobTitle = str(driver.find_element_by_id('BodyContent_inputTherapistJobTitle').get_attribute('value'))
    department = str(driver.find_element_by_id('BodyContent_inputTherapistDepartment').get_attribute('value'))
    if ((jobTitle == "")):
        jobTitle = "NIL"
    if (department == ""):
        department = "NIL"
    savedFile.write("Therapist Information" + "\n")
    savedFile.write("Job title: " + jobTitle + "\n")
    savedFile.write("Department: " + department + "\n")
    savedFile.close()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getTherapistInformationOnePage(driver, directory):

    '''
    Get all the therapist information in a single webpage

    Arguments:
        driver(obj): firefox webdriver instance in python 
        directory(str): Directory to store therapist information
    
    Returns:
        None
    '''
    number = 2
    while (number <= 6):
        therapistToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[5]/a"
        saveTherapistInformation(driver, therapistToken, directory)
        number +=1

def getAllTherapistInformation(driver, headerUrl):

    '''
    Get all the therapist information in a single webpage

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
            getTherapistInformationOnePage(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getTherapistInformationOnePage(driver, directory)
