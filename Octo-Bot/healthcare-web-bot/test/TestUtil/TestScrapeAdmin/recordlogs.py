import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestDriver.role import isAdmin
from TestUtil.TestScrapeAdmin.admin import viewAccountPages

from prettytable import PrettyTable

paginationXpath = "/html/body/form/div[4]/div[4]/div/div/table/tbody/tr[22]/td/table/tbody/tr/td["
scriptToken = "__doPostBack('ctl00$BodyContent$GridViewLogs','Page$"

getRecordsXpath = "/html/body/form/div[4]/div[4]/div/div/table/tbody/tr[22]/td/table/tbody/tr/td["

def getNumberRecordPages(driver):

    '''
    Obtains the number of pages that records logs webpage has
    
    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        number of pages that record logs webpage has
    '''
    number = 1
    scriptNumber = 2
    while(True):
        try:
            token = str(scriptNumber) + "]/a"
            newToken = getRecordsXpath + token
            print(newToken)
            driver.find_element_by_xpath(newToken).click()
            scriptNumber += 1
            number += 1
            time.sleep(3)
        except Exception as e:
            print(e)
            break
    return (number + 1)

def saveRecordLogs(driver, directory):
    
    '''
    Main logic behind the saving of record logs

    Arguments:
        driver(obj): firefox webdriver instance in python
        directory(str) : Directory to save record logs
    
    Returns:
        None
    '''
    print("Printing record logs...")
    outDirectory = directory + "/data/admin/RecordLogs.txt"
    savedFile = open(outDirectory, "a")
    table = PrettyTable(["Date/Time", "Subject", "Action", "Description"])
    table.align["Date/Time"] = "l"
    table.align["Subject"] = "l"
    table.align["Action"] = "l"
    table.align["Description"] = "l"
    soup = BeautifulSoup(driver.page_source,'html.parser')
    cla = soup.find("table", {"id" : "BodyContent_GridViewLogs"}).find_all("tr")
    for x in cla:
        storeData = []
        td = x.find_all("td")
        for element in td:
            data = element.get_text().strip()
            if data.isnumeric():
                continue
            else:
                storeData.insert(len(storeData), data)
        if len(storeData) != 4:
            continue
        else:
            table.add_row(storeData)
    savedFile.write(str(table))
    savedFile.write("\n")
    savedFile.close()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def getAllRecordLogs(driver, headerUrl):

    '''
    Obtains all the records logs 

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        None
    '''
    driver.get(headerUrl + "Admin/View-Logs/Account-Logs")
    time.sleep(2)
    driver.find_element_by_id("BodyContent_ButtonSearch").click()
    time.sleep(5)
    maxNumber = getNumberRecordPages(driver)
    print("Max number is: " + str(maxNumber))
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            saveRecordLogs(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
            time.sleep(3)
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/View-Logs/Account-Logs")
            time.sleep(10)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    saveRecordLogs(driver, directory)
