import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

directory = str(os.getcwd()) + "/config/measurement.json"

f = open(directory, "r")
data = json.loads(f.read())

""" Automates the injection of new records

getHeight function obtains the height data to be injected
getWeight function obtains the weight data to be injected
getTemperature function obtains the temperature data to be injected
getBloodPressure function obtains the blood pressure data to be injected
createNewReadings automate new data for each field
createNewRecords automate new data for all of the fields
"""
def getHeight():
    heightData = data["height"]
    heightInfo = []
    height = 0
    if (heightData["measurement"].isnumeric()):
        height = float(heightData["measurement"])
        if (height < 0 or height > 280):
            height = 0
            print("Invalid height. Height measurements set to default 0")
    else:
        height = 0
        print("Invalid height format. Height measurements set to default 0")
    heightInfo.append(str(height))
    title = heightData["title"]
    description = heightData["description"]
    if title == "":
        title = "NIL"
    if description == "":
        description = "NIL"
    heightInfo.append(title)
    heightInfo.append(description)
    return heightInfo 

def getWeight():
    weightData = data["weight"]
    weightInfo = []
    weight = 0
    if (weightData["measurement"].isnumeric()):
        weight = float(weightData["measurement"])
        if (weight < 0 or weight > 650):
            weight = 0
            print("Invalid weight. Weight measurements are set to default 0")
    else:
        weight = 0
        print("Invalid weight format. Weight measurements are set to default 0")
    weightInfo.append(str(weight))
    title = weightData["title"]
    description = weightData["description"]
    if title == "":
        title = "NIL"
    if description == "":
        description = "NIL"
    weightInfo.append(title)
    weightInfo.append(description)
    return weightInfo

def getTemperature():
    tempData = data["temperature"]
    tempInfo = []
    temp = 0
    if (tempData["measurement"].isnumeric()):
        temp = float(tempData["measurement"])
        if (temp < 0 or temp > 100):
            temp = 0
            print("Invalid Temperature. Temperature measurements are set to default 0")
    else:
        temp = 0
        print("Invalid temperature format. Temperature measurements are set to default 0") 
    tempInfo.append(str(temp))
    title = tempData["title"]
    description = tempData["description"]
    if title == "":
        title = "NIL"
    if description == "":
        description = "NIL"
    tempInfo.append(title)
    tempInfo.append(description)
    return tempInfo

def getBloodPressure():
    bloodPressureData = data["blood pressure"]
    bloodPressureInfo = []
    sys = 0
    di = 0
    bloodPressure = ""
    if (bloodPressureData["systolic"].isnumeric() and bloodPressureData["diastolic"].isnumeric()):
        sys = int(bloodPressureData["systolic"])
        di = int(bloodPressureData["diastolic"])
        if (sys < 0 or sys > 250):
            sys = 0
            print("Invalid systolic blood pressure. Systolic blood pressure measurement is set to default 0")
        elif (di < 0 or di > 250):
            di = 0
            print("Invalid diastolic blood pressure. Diastolic blood pressure measurement is set to default 0")
    else:
        sys = 0
        di = 0
        print("Invalid blood pressure format. Blood pressure measurement is set to default 0")
    bloodPressure = str(sys) + "/" + str(di)
    bloodPressureInfo.append(str(bloodPressure))
    title = bloodPressureData["title"]
    description = bloodPressureData["description"]
    if title == "":
        title = "NIL"
    if description == "":
        description = "NIL"
    bloodPressureInfo.append(title)
    bloodPressureInfo.append(description)
    return bloodPressureInfo

def createNewReadings(driver, data, token):
    driver.get('https://10.10.0.112/Patient/My-Records/New-Record')
    driver.find_element_by_id(token).click()
    driver.find_element_by_id('BodyContent_inputContent').send_keys(data[0])
    driver.find_element_by_id('BodyContent_inputTitle').send_keys(data[1])
    try:
        driver.find_element_by_id('BodyContent_inputDescription').clear().send_keys(data[2])
    except:
        driver.find_element_by_id('BodyContent_inputDescription').send_keys(data[2])
    driver.find_element_by_id('BodyContent_buttonSubmit').click()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def createNewRecords(driver):
    print("Injection new records in ...")
    print("Inject new records...")
    driver.find_element_by_id("A1").click()
    driver.find_element_by_id("navLinksSwitchRole").click()
    driver.find_element_by_id("BodyContent_buttonLoginPatient").click()
    driver.get("https://10.10.0.112/Patient/My-Records/New-Record")
    heightToken = 'RadioButtonTypeHeightMeasurement'
    weightToken = 'RadioButtonTypeWeightMeasurement'
    tempToken = 'RadioButtonTypeTemperatureReading'
    bloodPressureToken = 'RadioButtonTypeBloodPressureReading'
    weightInfo = getWeight()
    heightInfo = getHeight()
    tempInfo = getTemperature()
    bloodPressureInfo = getBloodPressure()
    createNewReadings(driver, weightInfo, weightToken)
    createNewReadings(driver, heightInfo, heightToken)
    createNewReadings(driver, tempInfo, tempToken)
    createNewReadings(driver, bloodPressureInfo, bloodPressureToken)

