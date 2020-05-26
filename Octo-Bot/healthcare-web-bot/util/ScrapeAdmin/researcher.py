import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from util.Driver.role import isAdmin
from util.ScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

'''Functions to get the Therapist info
Functions to progrssively crawl therapist info
'''

def saveResearcherInformation(driver, researcherToken, directory):
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
    number = 2
    while (number <= 6):
        therapistToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[6]/a"
        saveResearcherInformation(driver, therapistToken, directory)
        number +=1

def getAllResearcherInformation(driver):
    driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
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
            time.sleep(3)
        except:
            if (number == maxNumber):
                 break
            number += 1
            driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
            time.sleep(10)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getResearcherInformationOnePage(driver, directory)
