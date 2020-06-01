import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from util.ScrapeAdmin.admin import viewAccountPages

from prettytable import PrettyTable

""" Saves all record logs

saveRecordLogs function saves the record logs into a text file for each of the individual pages
getAllRecordLogs function iterates through all available pages and saves record logs
"""
paginationXpath = "/html/body/form/div[4]/div[4]/div/div/table/tbody/tr[22]/td/table/tbody/tr/td["

def saveRecordLogs(driver, directory):
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

def getAllRecordLogs(driver):
    driver.get("https://10.10.0.112/Admin/View-Logs/Account-Logs")
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
            saveRecordLogs(driver, directory)
            driver.find_element_by_xpath(Xpath).click()
            number += 1
        except:
            if (number == maxNumber):
                break
            number += 1
            driver.get("https://10.10.0.112/Admin/View-Logs/Account-Logs")
            time.sleep(2)
            driver.find_element_by_id("BodyContent_ButtonSearch").click()
            time.sleep(3)
            Xpath = paginationXpath + token
            driver.find_element_by_xpath(Xpath).click()
    saveRecordLogs(driver, directory)
