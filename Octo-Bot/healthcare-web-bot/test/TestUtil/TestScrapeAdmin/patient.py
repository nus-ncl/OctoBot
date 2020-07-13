import os
import time

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

def savePatientInformation(driver, patientToken, directory):

    '''
    Main Logic behind saving patient information
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        patientToken(str) : Token used to find xpath by driver
        directory(str) : Directory used to save patient information

    Returns:
        None
    '''
    print("Getting patient information...")
    time.sleep(3)
    driver.find_element_by_xpath(patientToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_labelPatientNRIC").text)
    outDirectory = directory + "/data/admin/" + str(nric) + ".txt"
    savedFile = open(outDirectory, "a")
    nameNOK = str(driver.find_element_by_id('BodyContent_inputPatientNokName').get_attribute("value"))
    contactNOK = str(driver.find_element_by_id('BodyContent_inputPatientNokContact').get_attribute('value'))
    if (nameNOK == ""):
        nameNOK = "NIL"
    if (contactNOK == ""):
        contactNOK = "NIL"
    savedFile.write("Next-of-Kin name: " + nameNOK + "\n")
    savedFile.write("Next-of-Kin contact: " + contactNOK + "\n")
    savedFile.write("Emergency Theraphist: " + "\n")
    isTherapistNeeded = True
    table = PrettyTable(["NRIC", "First name", "Last name", "Job Title", "Department"])
    table.padding_width = 1
    soup = BeautifulSoup(driver.page_source,'html.parser')
    cla = soup.find("table", {"id" : "BodyContent_GridViewTherapists2"}).find_all("tr")
    for element in cla:
        line = element.find_all("td")
        data = ""
        storeData = []
        for x in line:
            word = str(x.get_text()).strip()
            if word == "Remove":
                continue
            else:
                word = str(x.get_text()).strip()
                storeData.insert(len(storeData), word)
                data += word + " "
        if data == "":
            continue
        elif "No Results." in data:
            isTherapistNeeded = False
        else:
            table.add_row(storeData)
    if isTherapistNeeded:
        savedFile.write(str(table))
        savedFile.write("\n")
    else:
        savedFile.write("There are no assigned Therapist." + "\n")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getPatientInformationOnePage(driver, directory):

    '''
    Obtain patient information in a single webpage
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        directory(str) : Directory used to save patient information
    
    Returns:
        None
    '''
    number = 2
    while (number <= 6):
        patientToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[4]/a"
        savePatientInformation(driver, patientToken, directory)
        number +=1

def getAllPatientInformation(driver, headerUrl):

    '''
    Obtain patient information from all the webpages
    
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
            getPatientInformationOnePage(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getPatientInformationOnePage(driver, directory)
