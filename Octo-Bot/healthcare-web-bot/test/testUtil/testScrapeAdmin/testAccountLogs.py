import os
import time

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from testUtil.testDriver.testRole import isAdmin
from testUtil.testScrapeAdmin.testAdmin import viewAccountPages

paginationXpath = "/html/body/form/div[4]/div[4]/div/div/table/tbody/tr[22]/td/table/tbody/tr/td["

def saveAccountLogs(driver, directory):
    print("Getting account logs...")
    outDirectory = directory + "/data/admin/AccountLogs.txt"
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

def getAllAccountLogs(driver):
    driver.get("https://10.10.0.112/Admin/View-Logs/Record-Logs")
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
            saveAccountLogs(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
            time.sleep(3)
        except:
            number += 1
            driver.get("https://10.10.0.112/Admin/View-Logs/Record-Logs")
            time.sleep(10)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    saveAccountLogs(driver, directory)
