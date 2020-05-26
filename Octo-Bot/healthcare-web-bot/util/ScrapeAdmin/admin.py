import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from util.Driver.role import isAdmin

base_adminUrl = "https://10.10.0.112/Admin/Dashboard"
paginationXpath =  "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr[7]/td/table/tbody/tr/td["
personalButtonXpath = "/html/body/form/div[4]/div[2]/div/div/table/tbody/tr["

def viewAccountPages(driver):
    number = 0
    soup = BeautifulSoup(driver.page_source,'html.parser')
    # print(soup)
    cla = soup.find("tr", {"class": "pagination-gridview"}).find("tbody").find_all("td")
    for element in cla:
        number = int(element.text)
    return number

