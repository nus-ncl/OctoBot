import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from testUtil.testScrapeAdmin.testadmin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

""" Saves all the personal information for each user

savePersonalInformation function obtains all the information for each user
getPersonalInformationOnePage obtains all the personal information for each user in one page
getAllPersonalInformation saves all the personal information for each user into individual text files
"""

def savePersonalInformation(driver, personalToken, directory):
    print("Printing personal information...")
    time.sleep(3)
    driver.find_element_by_xpath(personalToken).click()
    time.sleep(3)
    nric = str(driver.find_element_by_id("BodyContent_inputPersonalNRIC").get_attribute("value"))
    dob = str(driver.find_element_by_id("BodyContent_inputPersonalDoB").get_attribute("value"))
    firstName = str(driver.find_element_by_id("BodyContent_inputPersonalFirstName").get_attribute("value"))
    lastName = str(driver.find_element_by_id("BodyContent_inputPersonalLastName").get_attribute("value"))
    cob = str(driver.find_element_by_id("BodyContent_inputPersonalCountryofBirth").get_attribute("value"))
    nationality = str(driver.find_element_by_id("BodyContent_inputPersonalNationality").get_attribute("value"))
    sex = str(driver.find_element_by_id("BodyContent_inputPersonalSex").get_attribute("value"))
    gender = str(driver.find_element_by_id("BodyContent_inputPersonalGender").get_attribute("value"))
    maritalStatus = str(driver.find_element_by_id("BodyContent_inputPersonalMaritalStatus").get_attribute("value"))
    outDirectory = directory + "/data/admin/" + nric + ".txt"
    newFile = open(outDirectory,"a")
    newFile.write("NRIC: " + nric)
    newFile.write("\n")
    newFile.write("NRIC: " + nric + "\n")
    newFile.write("DOB: " + dob + "\n")
    newFile.write("First Name: " + firstName + "\n")
    newFile.write("Last Name: " + lastName + "\n")
    newFile.write("Coountry of Birth: " + cob + "\n")
    newFile.write("Nationality: " + nationality + "\n")
    newFile.write("Gender: " + gender + "\n")
    newFile.write("Sex: " + sex + "\n")
    newFile.write("Marital status: " + maritalStatus + "\n")
    newFile.close()
    driver.find_element_by_class_name("close").click()

def getPersonalInformationOnePage(driver, directory):
    number = 2
    while (number <= 6):
        try:
            personalToken = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[" + str(number) + "]/td[2]/a"
            savePersonalInformation(driver, personalToken, directory)
            number += 1
        except:
            number +=1

def getAllPersonalInformation(driver):
    driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
    time.sleep(3)
    maxNumber = viewAccountPages(driver)
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            getPersonalInformationOnePage(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getPersonalInformationOnePage(driver,directory)
