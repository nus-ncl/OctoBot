import os
import time

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from TestUtil.TestScrapeAdmin.admin import viewAccountPages

paginationXpath = "/html/body/form/div[4]/div[4]/div/div/table/tbody/tr[22]/td/table/tbody/tr/td["

def savePermissionLogs(driver, directory):

    '''
    Main Logic to save permission Logs
    
    Arguments:
        driver(obj): firefox webdriver instance in python
        directory(str) : Directory to save permission logs
    
    Returns:
        None
    '''
    print("Getting permission logs...")
    outDirectory = directory + "/data/admin/PermissionLogs.txt"
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

def getAllPermissionLogs(driver, headerUrl):

    '''
    Obtain all permission logs
    
    Arguments:
        driver(obj): firefox webdriver instance in python

    Returns:
        None
    '''
    driver.get(headerUrl + "Admin/View-Logs/Permission-Logs")
    time.sleep(2)
    driver.find_element_by_id("BodyContent_ButtonSearch").click()
    time.sleep(3)
    maxNumber = viewAccountPages(driver)
    number = 2
    directory = str(os.getcwd())
    while (number < maxNumber + 1):
        try:
            token = str(number) + "]/a"
            Xpath = paginationXpath + token
            savePermissionLogs(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get(headerUrl + "Admin/View-Logs/Permission-Logs")
            time.sleep(2)
            driver.find_element_by_id("BodyContent_ButtonSearch").click()
            time.sleep(3)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    savePermissionLogs(driver, directory)
