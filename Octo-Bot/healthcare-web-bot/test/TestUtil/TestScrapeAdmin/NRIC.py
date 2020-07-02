import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["

def getAllNricInPage(driver, file, directory):

    '''
    Obtains all the NRIC in a single webpage

    Arguments:
        driver(obj): firefox webdriver instance in python
        file(str) : Filename to save the NRICs to
        directory(str): Directory to save all the NRIC to
    
    Returns:
        None
    '''
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

    '''
    Creates the file for storing the NRICs
    
    Arguments:
        directory(str): Directory that has to be created for storing the file

    Return:
        file object of the created file 
    '''
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

def getAllNric(driver, headerUrl):
    
    '''
    Obtains all the NRIC that is available in the database

    Arguments:
        driver(obj): firefox webdriver instance in python

    Returns:
        None
    '''
    driver.find_element_by_id('BodyContent_buttonLoginAdmin').click()
    driver.get(headerUrl + "Admin/Manage-Accounts/View")
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
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/Manage-Accounts/View")
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    getAllNricInPage(driver, file, directory)
    file.close()
