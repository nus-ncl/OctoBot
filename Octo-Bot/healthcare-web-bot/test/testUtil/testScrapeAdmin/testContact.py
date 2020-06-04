import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from testUtil.testDriver.testRole import isAdmin
from testUtil.testScrapeAdmin.testAdmin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

'''Functions to get the contact info
Functions to progrssively crawl contact info
'''
def saveContactInformation(driver, contactToken, directory):
    print("Getting contact information...")
    time.sleep(3)
    driver.find_element_by_xpath(contactToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_labelContactNRIC").text)
    outDirectory = directory + "/data/admin/" + str(nric) + ".txt"
    savedFile = open(outDirectory, "a")
    address = str(driver.find_element_by_id('BodyContent_inputAddress').get_attribute('value'))
    postalCode = str(driver.find_element_by_id('BodyContent_inputPostalCode').get_attribute('value'))
    email = str(driver.find_element_by_id('BodyContent_inputEmailAddress').get_attribute('value'))
    contactNumber = str(driver.find_element_by_id('BodyContent_inputContactNumber').get_attribute('value'))
    savedFile.write("Address: " + address + "\n")
    savedFile.write("Postal code: " + postalCode + "\n")
    savedFile.write("Email: " + email + "\n")
    savedFile.write("Contact Number: " + contactNumber + "\n")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # driver.find_element_by_class_name("close").click()
def getContactInformationOnePage(driver, directory):
    number = 2
    while (number <= 6):
        contactToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[3]/a"
        saveContactInformation(driver, contactToken, directory)
        number +=1

def getAllContactInformation(driver):
    time.sleep(3)
    driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
    maxNumber = viewAccountPages(driver)
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            getContactInformationOnePage(driver, directory)
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
    getContactInformationOnePage(driver, directory)
