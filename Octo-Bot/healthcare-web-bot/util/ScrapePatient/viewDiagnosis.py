import time
import os
from bs4 import BeautifulSoup

directory = str(os.getcwd())
saveDirectory = directory + "/data/patient/"

def createDirectory(savedFolder):

    '''
    Creates directory for storing diagnosis information
    
    Arguments:
        savedFolder(str) : Filename of where diagnosis information is to be stored
    
    Returns:
        None
    '''
    if (os.path.isdir(savedFolder) == False):
        try:
            os.makedirs(savedFolder, exist_ok = True)
        except Exception as e:
            print(str(e))
            print("Path creation failed!")  
    else:
        return

def checkResults(driver):
    
    '''
    Verifies if there are diagnosis information to be scrapped
    
    Arguments:
        driver(obj): firefox webdriver instance in python 
    
    Returns:
        Tru if there are no diagnosis information. Else, return False
    '''
    results = BeautifulSoup(driver.page_source, 'html.parser')
    cla = str(results.text)
    if "You have no Diagnosis attributed to you" in cla:
        return True
    else:
        return False

def getDiagnosisInformation(driver, patientNRIC, headerUrl):

    '''
    Main Logic to obtain diagnosis information

    Arguments:
        driver(obj): firefox webdriver instance in python 
        patientNRIC(str) : NRIC of the patient that we are scrapping diagnosis information for
    
    Returns:
        None
    '''
    driver.get(headerUrl + "Patient/My-Diagnoses")
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
