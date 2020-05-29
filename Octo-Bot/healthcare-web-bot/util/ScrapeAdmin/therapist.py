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
def saveTherapistInformation(driver, therapistToken, directory):
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
    number = 2
    while (number <= 6):
        therapistToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[5]/a"
        saveTherapistInformation(driver, therapistToken, directory)
        number +=1

def getAllTherapistInformation(driver):
    driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
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
            time.sleep(3)
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
            time.sleep(10)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getTherapistInformationOnePage(driver, directory)
