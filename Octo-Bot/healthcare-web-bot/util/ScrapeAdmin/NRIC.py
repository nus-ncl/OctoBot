import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from util.Driver.role import isAdmin
from util.ScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

''' These are functions to obtain all the NRIC
These are the functions used to progrssively obtain NRIC for all pages
'''
def getAllNricInPage(driver, file, directory):
    print("Getting NRIC information...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cla = soup.find("table", {"class": "table table-sm table-responsive-sm"}).find("tbody").find_all("td")
    for element in cla:
        data = str(element.text).strip()
        if (data == "View"  or data.isnumeric()):
            continue
        else:
            file.write(data)
            file.write("\n")

def createFile(directory):
    pathName = directory + "/data/admin"
    if (os.path.isdir(pathName) == False):
        try:
            os.makedirs(pathName, exist_ok = True)
        except Exception as e:
            print(str(e))
            print("Path creation failed!")    
    finalDirectory = directory + "/data/admin/NRIC.txt"
    if (os.path.isfile(finalDirectory)):
        os.remove(finalDirectory)
    file = open(finalDirectory, "a")
    file.write("The list of NRIC are:\n")
    return file

def getAllNric(driver):
    if isAdmin(driver):
        driver.find_element_by_id('BodyContent_buttonLoginAdmin').click()
        driver.get("https://10.10.0.112/Admin/Manage-Accounts/View")
        maxNumber = viewAccountPages(driver)
        number = 2
        directory = str(os.getcwd())
        file = createFile(directory)
        while (number < maxNumber + 1):
            try:
                token = str(number) + "]/a"
                Xpath = paginationXpath + token
                getAllNricInPage(driver, file, directory)
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
        getAllNricInPage(driver, file, directory)
        file.close()
