import time
import os
from bs4 import BeautifulSoup

directory = str(os.getcwd())
saveDirectory = directory + "/data/patient/"

""" Helper function to scrape all the diagnosis information for the patient

createDirectory creates the directory for storing the scrapped diagnosis information
checkResults checks if there are any diagnosis results for the patient
getDiagnosisInformation scrapes all the diagnosis information for the patient
"""
def createDirectory(savedFolder):
    if (os.path.isdir(savedFolder) == False):
        try:
            os.makedirs(savedFolder, exist_ok = True)
        except Exception as e:
            print(str(e))
            print("Path creation failed!")  
    else:
        return

def checkResults(driver):
    results = BeautifulSoup(driver.page_source, 'html.parser')
    cla = str(results.text)
    if "You have no Diagnosis attributed to you" in cla:
        return True
    else:
        return False

def getDiagnosisInformation(driver, patientNRIC):
    driver.get("https://10.10.0.112/Patient/My-Diagnoses")
    time.sleep(2)
    savedDirectory = saveDirectory + str(patientNRIC) + "/"
    createDirectory(savedDirectory)
    savedFileName = savedDirectory + "diagnosis.txt"
    f = open(savedFileName, "a")
    if checkResults(driver) == True:
        print("There is no diagnosis for " + str(patientNRIC))
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser').find("table", {"id" : "BodyContent_GridViewPatientDiagnoses"}).find_all("tr")
        for x in soup:
            data = x.find_all("td")
            info = []
            for y in data:
                line = str(y.text).strip()
                info.append(line)
            if len(info) == 0:
                continue
            else:
                f.write("Code: " + str(info[0]) + "\n")
                f.write("   -Description: " + str(info[1]) + "\n")
                f.write("   -Category: " + str(info[2]) + "\n")
                f.write("   -Assigned by: " + str(info[3]) + "\n")
                f.write("   -Start: " + str(info[4]) + "\n")
                f.write("   -End: " + str(info[5]) + "\n")
