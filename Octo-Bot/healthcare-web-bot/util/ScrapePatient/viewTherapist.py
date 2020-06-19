import time
import os
from bs4 import BeautifulSoup

directory = str(os.getcwd())
saveDirectory = directory + "/data/patient/"

def createDirectory(savedFolder):
    
    '''
    Creates directory for storing therapist information

    Arguments:
        savedFolder(str): Name of folder for saving the therapist information
    
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
    Checks if there are therapist information to be scrapped

    Arguments:
        driver(obj): firefox webdriver instance in python 
    
    Returns:
        True if there are no results. Else, returns False
    '''
    results = BeautifulSoup(driver.page_source, 'html.parser')
    cla = str(results.text)
    if "Search returned no results" in cla:
        return True
    else:
        return False

def getTherapistInformation(driver, patientNRIC, headerUrl):

    '''
    Main logic for obtaining therapist information
    
    Arguments:
        driver(obj): firefox webdriver instance in python 
        patientNRIC(str): NRIC of patient
    
    Returns:
        None
    '''
    driver.get(headerUrl + "Patient/My-Therapists")
    time.sleep(2)
    savedDirectory = saveDirectory + str(patientNRIC) + "/"
    createDirectory(savedDirectory)
    savedFileName = savedDirectory + "therapist.txt"
    f = open(savedFileName, "a")
    if checkResults(driver) == True:
        print("There is no therapist information for " + str(patientNRIC))
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser').find("table", {"id" : "BodyContent_GridViewTherapist"}).find_all("tr")
        for x in soup:
            data = x.find_all("td")
            info = []
            for y in data:
                line = str(y.text).strip()
                if line == "View":
                    continue
                else:
                    info.append(line)
            if len(info) == 0:
                continue
            else:
                f.write("Therapist Name: " + str(info[0]) + "\n")
                f.write("     -Title: " + str(info[1]) + "\n")
                f.write("     -Department: " + str(info[2]) + "\n")
                