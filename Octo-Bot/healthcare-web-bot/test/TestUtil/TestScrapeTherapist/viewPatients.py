import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable

directory = str(os.getcwd())
saveDirectory = directory + "/data/therapist"

scriptToken = "__doPostBack('ctl00$BodyContent$GridViewPatient$ctl0"

def createDirectory(savedFolder):
    '''
    Creates directory for storing patient information

    Arguments:
        savedFolder(str): Name of folder for saving the patient information
    
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

def numberOfEnteries(driver):

    '''
    Obtains the number of enteries of therapist information

    Arguments:
        driver(obj): firefox webdriver instance in python 
    
    Returns:
        Total number of enteries for therapist information
    '''
    try:
        soup = BeautifulSoup(driver.page_source,'html.parser')
        cla = soup.find("table", {"id" : "BodyContent_GridViewPatient"}).find_all("tr")
        number = 0
        for x in cla:
            number += 1
        return (number  - 1)
    except:
        return 0


def loginTherapist(driver, headerUrl):

    '''
    Assist in login of therapist and directing them to the homepage of therapist
    
    Arguments:
        driver(obj): firefox webdriver instance in python 
    
    Returns:
        None
    '''
    driver.find_element_by_id('BodyContent_buttonLoginTherapist').click()
    driver.get(headerUrl + "Therapist/My-Patients/View")

def checkResults(driver):

    '''
    Checks if there are patient information to be scrapped

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

def getPersonalInformation(driver, therapistNRIC):

    '''
    Main Logic to obtain the personal information of patients
    
    Arguments:
        driver(obj): firefox webdriver instance in python 
        therapistNRIC(str) : NRIC of therapist
    
    Returns NRIC of patient
    '''
    savedFolder = saveDirectory + "/" + str(therapistNRIC)
    createDirectory(savedFolder)
    nric = str(driver.find_element_by_id('BodyContent_inputNRIC').get_attribute('value'))
    print("NRIC is: " + str(nric))
    if (nric == ""):
        return
    else:
        savedFileName = savedFolder + "/" + str(nric) + ".txt"
        f = open(savedFileName, "a")
        dob = str(driver.find_element_by_id('BodyContent_DateofBirth').get_attribute('value'))
        firstName = str(driver.find_element_by_id('BodyContent_FirstName').get_attribute('value'))
        lastName = str(driver.find_element_by_id('BodyContent_LastName').get_attribute('value'))
        country = str(driver.find_element_by_id('BodyContent_CountryofBirth').get_attribute('value'))
        nationality = str(driver.find_element_by_id('BodyContent_Nationality').get_attribute('value'))
        sexuality = str(driver.find_element_by_id('BodyContent_Sex').get_attribute('value'))
        gender = str(driver.find_element_by_id('BodyContent_Gender').get_attribute('value'))
        maritialStatus = str(driver.find_element_by_id('BodyContent_MaritalStatus').get_attribute('value'))
        address = str(driver.find_element_by_id('BodyContent_Address').get_attribute('value'))
        postalCode = str(driver.find_element_by_id('BodyContent_PostalCode').get_attribute('value'))
        email = str(driver.find_element_by_id('BodyContent_EmailAddress').get_attribute('value'))
        contactNumber = str(driver.find_element_by_id('BodyContent_ContactNumber').get_attribute('value'))
        NOKName = str(driver.find_element_by_id('BodyContent_NOKName').get_attribute('value'))
        NOKContact = str(driver.find_element_by_id('BodyContent_NOKContact').get_attribute('value'))
        f.write("NRIC: " + str(nric) + "\n")
        f.write("Date of Birth: " + str(dob) + "\n")
        f.write("First Name: " + str(firstName) + "\n")
        f.write("Last Name: " + str(lastName) + "\n")
        f.write("Country of Birth: " + str(country) + "\n")
        f.write("Nationality: " + str(nationality) + "\n")
        f.write("Sexuality: " + str(sexuality) + "\n")
        f.write("Gender: " + str(gender) + "\n")
        f.write("Maritial Staus: " + str(maritialStatus) + "\n")
        f.write("Address: " + str(address) + "\n")
        f.write("Postal code: " + str(postalCode) + "\n")
        f.write("Email: " + str(email) + "\n")
        f.write("Contact Number " + str(contactNumber) + "\n")
        f.write("Next-of-kin Name: " + str(NOKName) + "\n")
        f.write("Next-of-kin Contact: " + str(NOKContact) + "\n")
        return nric

def getPermissions(driver, therapistNRIC, nric):

    '''
    Obtains the permissions of the therapist

    Arguments:
        driver(obj): firefox webdriver instance in python 
        therapistNRIC(str) : NRIC of the therapist
        nric(str): NRIC of the patient
    
    Returns:
        None
    '''
    if (nric == None):
        return
    else:
        savedFolder = saveDirectory + "/" + str(therapistNRIC)
        savedFileName = savedFolder + "/" + str(nric) + ".txt"
        f = open(savedFileName, "a")
        print("NRIC FOR PERMISSIONS: " + str(nric))
        heightPermission = True
        weightPermission = True
        temperaturePermission = True
        bpPermission = True
        ecgPermission = True
        mriPermission = True
        xrayPermission = True
        gaitPermission = True
        if driver.find_element_by_id('CheckBoxTypeHeightMeasurementApproved').get_attribute('checked') == None:
            heightPermission = False
        if driver.find_element_by_id('CheckBoxTypeWeightMeasurementApproved').get_attribute('checked') == None:
            weightPermission = False
        if driver.find_element_by_id('CheckBoxTypeTemperatureReadingApproved').get_attribute('checked') == None:
            temperaturePermission = False
        if driver.find_element_by_id('CheckBoxTypeBloodPressureReadingApproved').get_attribute('checked') == None:
            bpPermission = False
        if driver.find_element_by_id('CheckBoxTypeECGReadingApproved').get_attribute('checked') == None:
            ecgPermission = False
        if driver.find_element_by_id('CheckBoxTypeMRIApproved').get_attribute('checked') == None:
            mriPermission = False
        if driver.find_element_by_id('CheckBoxTypeXRayApproved').get_attribute('checked') == None:
            xrayPermission = False
        if driver.find_element_by_id('CheckBoxTypeGaitApproved').get_attribute('checked') == None:
            gaitPermission = False
        f.write("Height Permissions: " + str(heightPermission) + "\n")
        f.write("Weight Permissions: " + str(weightPermission) + "\n")
        f.write("Temperature Permissions: " + str(temperaturePermission) + "\n")
        f.write("Blood Pressure Permissions: " + str(bpPermission) + "\n")
        f.write("ECG Permissions: " + str(ecgPermission) + "\n")
        f.write("MRI Permissions: " + str(mriPermission) + "\n")
        f.write("X-Ray Permissions: " + str(xrayPermission) + "\n")
        f.write("Gait Permissions: " + str(gaitPermission) + "\n")

def getDiagnosis(driver, therapistNRIC, nric):

    '''
    Obtains the diagnosis of the therapist

    Arguments:
        driver(obj): firefox webdriver instance in python 
        therapistNRIC(str) : NRIC of the therapist
        nric(str): NRIC of the patient
    
    Returns:
        None
    '''
    if nric is None:
        return
    else:
        savedFolder = saveDirectory + "/" + str(therapistNRIC)
        savedFileName = savedFolder + "/" + str(nric) + ".txt"
        f = open(savedFileName, "a")
        print("NRIC for diagnosis: " + str(nric))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cla = soup.find("table", {"id" : "BodyContent_GridViewPatientDiagnoses"})
        if cla is None:
            return
        else:
            data = cla.find_all("tr")
            for rows in data:
                details = rows.find_all("td")
                info = []
                for x in details:
                    line = str(x.text).strip()
                    info.append(line)
                if len(info) == 6:
                    codeLine = "Code: " + str(info[0]) + "\n"
                    descriptionLine = "    -Description: " + str(info[1]) + "\n"
                    categoryLine = "    -Category: " + str(info[2]) + "\n"
                    assignedLine = "    -Assigned by: " + str(info[3]) + "\n"
                    startLine = "    -Start: " + str(info[4]) + "\n"
                    endLine = "    -End: " + str(info[5]) + "\n"
                    f.write(codeLine)
                    f.write(descriptionLine)
                    f.write(categoryLine)
                    f.write(assignedLine)
                    f.write(startLine)
                    f.write(endLine)

def iteratePage(driver, therapistNRIC):
    
    '''
    Main Logic behing obtaining all the information of patients

    Arguments:
        driver(obj): firefox webdriver instance in python 
        therapistNRIC(str): NRIC of the therapist
    
    Returns:
        None
    '''
    # createDirectory()
    if checkResults(driver) == True:
        print("There are no patients for " + str(therapistNRIC))
    else:
        totalEnteries = numberOfEnteries(driver)
        number = 0
        try:
            while (number < totalEnteries + 1):
                personalToken = str(number + 2) + "$LinkButtonViewInformation','')"
                personalScript = scriptToken + personalToken
                driver.execute_script(personalScript)
                nric = getPersonalInformation(driver, therapistNRIC)
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(3)
                permissionToken = str(number + 2) + "$LinkButtonViewPermission','')"
                permissionScript = scriptToken + permissionToken
                driver.execute_script(permissionScript)
                getPermissions(driver, therapistNRIC, nric)
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(3)
                diagnosisToken = str(number + 2) + "$LinkButtonViewDiagnosis','')"
                diagnosisScript = scriptToken + diagnosisToken
                driver.execute_script(diagnosisScript)
                getDiagnosis(driver, therapistNRIC, nric)
                time.sleep(3)
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(3)
                number += 1
        except:
            return
