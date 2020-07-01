import time

from FileParser import getPatientCredentials, getTherapistCredentials
from selenium import webdriver
from selenium.webdriver.remote.command import Command

logoutScript = "__doPostBack('ct100$ct113','')"
driverAlive = "alive"
driverDead = "dead"

def adminLogin(url, driver, username, password):

    '''
    Main logic behind logging into an admin role

    Arguments:
        url(str): target url
        driver(obj): Firefox webdriver instance in python 
        username(str): Username used for logging in
        password(str): Password used for logging in
    
    Returns:
        boolean value, depending on whether login is a success
    '''
    username_box = driver.find_element_by_id('BodyContent_inputNRIC')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('BodyContent_inputPassword')
    password_box.send_keys(password)
    driver.find_element_by_id('BodyContent_ButtonLogin').click()
    time.sleep(3)
    try:
        if (str(driver.current_url) == url + "Role-Selection"):
            driver.find_element_by_id('BodyContent_buttonLoginAdmin').click()
            print("Logged in as admin!")
            return True
        elif (str(driver.current_url) == url + "Admin/Dashboard"):
            print("Logged in as admin!")
            return True
        else:
            return False
    except:
        print("There is no admin role for user")
        return False

def patientLogin(url, driver, username, password):

    '''
    Main logic behind logging into a patient role

    Arguments:
        url(str): target url
        driver(obj): Firefox webdriver instance in python 
        username(str): Username used for logging in
        password(str): Password used for logging in
    
    Returns:
        boolean value, depending on whether login is a success
    '''
    username_box = driver.find_element_by_id('BodyContent_inputNRIC')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('BodyContent_inputPassword')
    password_box.send_keys(password)
    driver.find_element_by_id('BodyContent_ButtonLogin').click()
    time.sleep(3)
    try:
        if (str(driver.current_url) == url + "Role-Selection"):
            driver.find_element_by_id('BodyContent_buttonLoginPatient').click()
            print("Logged in as patient!")
            return True
        elif (str(driver.current_url) == url + "Patient/Dashboard"):
            print("Logged in as patient!")
            return True
        else:
            return False
    except:
        print("There is no patient role for user")
        return False

def therapistLogin(url, driver, username, password):

    '''
    Main logic behind logging into an therapist role

    Arguments:
        url(str): target url
        driver(obj): Firefox webdriver instance in python 
        username(str): Username used for logging in
        password(str): Password used for logging in
    
    Returns:
        boolean value, depending on whether login is a success
    '''
    username_box = driver.find_element_by_id('BodyContent_inputNRIC')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('BodyContent_inputPassword')
    password_box.send_keys(password)
    driver.find_element_by_id('BodyContent_ButtonLogin').click()
    time.sleep(3)
    try:
        if (str(driver.current_url) == url + "Role-Selection"):
            driver.find_element_by_id('BodyContent_buttonLoginTherapist').click()
            print("Logged in as therapist!")
            return True
        elif (str(driver.current_url) == url + "Therapist/Dashboard"):
            print("Logged in as therapist!")
            return True
        else:
            return False
    except:
        print("There is no therapist role for user")
        return False
        
def getDriver(url):

    '''
    Main logic behind creating a driver object to use FireFox web browser

    Arguments:
        url(str): Target url
    
    Returns:
        Firefox webdriver instance in python
    '''
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    firefox_options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(firefox_options = firefox_options,firefox_profile = profile)
    driver.get(url)
    return driver

def getDriverStatus(driver):
    try:
        driver.execute(Command.STATUS)
        return driverAlive
    except:
        return driverDead
        
def registerPatientAccount(url, driver):

    '''
    Main logic used for registering a patient account

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Return:
        None
    '''
    patientCredentials = getPatientCredentials()
    driver.get(url + "Admin/Manage-Accounts/Register")
    nric = patientCredentials[0]
    dob = patientCredentials[1]
    firstName = patientCredentials[2]
    lastName = patientCredentials[3]
    address = patientCredentials[4]
    email = patientCredentials[5]
    postalcode = patientCredentials[6]
    contactNumber = patientCredentials[7]
    password = patientCredentials[8]
    driver.find_element_by_id('BodyContent_inputNRIC').send_keys(nric)
    dateBox = driver.find_element_by_id('BodyContent_inputDoB')
    dateBox.click()
    dateBox.send_keys(dob)
    driver.find_element_by_id('BodyContent_inputFirstName').send_keys(firstName)
    driver.find_element_by_id('BodyContent_inputLastName').send_keys(lastName)
    driver.find_element_by_id('BodyContent_inputAddress').send_keys(address)
    driver.find_element_by_id('BodyContent_inputPostalCode').send_keys(postalcode)
    driver.find_element_by_id('BodyContent_inputEmail').send_keys(email)
    driver.find_element_by_id('BodyContent_inputContactNumber').send_keys(contactNumber)
    driver.find_element_by_id('BodyContent_inputPassword').send_keys(password)
    driver.find_element_by_id('BodyContent_inputPasswordConfirm').send_keys(password)
    driver.find_element_by_id('BodyContent_inputCountryofBirth').send_keys('Afghanistan')
    driver.find_element_by_id('BodyContent_inputNationality').send_keys('Afghan')
    driver.find_element_by_id('BodyContent_buttonRegister').click()

def assignTherapist(url, driver):
    '''
    Main logic behind assigning therapist for the patient

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    patientCredentials = getPatientCredentials()
    therapistCredentials = getTherapistCredentials()
    driver.get(url + 'Admin/Manage-Accounts/View')
    driver.find_element_by_id('BodyContent_TextboxSearch').send_keys(patientCredentials[0])
    driver.find_element_by_id('BodyContent_ButtonSearch').click()
    time.sleep(10)
    patientScript = "__doPostBack('ctl00$BodyContent$GridViewAccounts$ctl02$ctl02','')"
    driver.execute_script(patientScript)
    time.sleep(10)
    driver.find_element_by_id('BodyContent_TextboxSearchTherapist').send_keys(therapistCredentials[0])
    driver.find_element_by_id('BodyContent_ButtonSearchTherapist').click()
    therapistScript = "__doPostBack('ctl00$BodyContent$GridViewTherapists$ctl02$ctl00','')"
    driver.execute_script(therapistScript)
    time.sleep(10)
    logoutScript = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(logoutScript)
    driver.close()
    driver.quit()
    print(" -Therapist assigned to patient")

def createNewRecord(url, driver):

    '''
    Main logic behind creating new records for patient

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    driver.get(url + 'Patient/My-Records/New-Record')
    patientCredentials = getPatientCredentials()
    information = str(patientCredentials[9]).lower()
    data = patientCredentials[10]
    if information == "height":
        driver.find_element_by_id('RadioButtonTypeHeightMeasurement').click()
    elif information == "weight":
        driver.find_element_by_id('RadioButtonTypeWeightMeasurement').click()
    elif information == "temperature":
        driver.find_element_by_id('RadioButtonTypeTemperatureReading').click()
    elif information == "bp":
        driver.find_element_by_id('RadioButtonBloodPressureReading').click()
    else:
        print("Invalid data type! Please use a valid data type(height/weight/temperature/bp)")
        return
    driver.find_element_by_id('BodyContent_inputContent').send_keys(data)
    driver.find_element_by_id('BodyContent_inputTitle').send_keys('Test Data')
    driver.find_element_by_id('BodyContent_buttonSubmit').click()
    logoutScript = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(logoutScript)
    driver.close()
    driver.quit()
    print(" -Records created for new patient")

def requestPermissions(url, driver):

    '''
    Main logic behind requesting permission for therapist to access patient records

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    try:
        patientCredentials = getPatientCredentials()
        therapistCredentials = getTherapistCredentials()
        information = str(patientCredentials[9]).lower()
        driver.get(url + 'Therapist/My-Patients/New-Request')
        driver.find_element_by_id('BodyContent_TextboxSearch').send_keys(patientCredentials[0])
        driver.find_element_by_id('BodyContent_ButtonSearch').click()
        time.sleep(10)
        driver.find_element_by_id('BodyContent_GridViewPatient_LinkButtonRequest_0').click()
        if information == "height":
            driver.find_element_by_id('CheckBoxTypeHeightMeasurement').click()
        elif information == "weight":
            time.sleep(10)
            weightBox = driver.find_element_by_id('CheckBoxTypeWeightMeasurement').click()
        elif information == "temperature":
            time.sleep(10)
            driver.find_element_by_id('CheckBoxTypeTemperatureMeasurement').click()
        elif information == "bp":
            time.sleep(2)
            driver.find_element_by_id('CheckBoxTypeBloodPressureMeasurement').click()
        else:
            print("No such permissions")
            return
        driver.find_element_by_id('BodyContent_buttonRequest').click()
        logoutScript = "__doPostBack('ctl00$ctl13','')"
        driver.execute_script(logoutScript)
        driver.close()
        driver.quit()
        print(" -Therapist request for permission")
    except:
        driver.close()
        driver.quit()
        print("Permission already obtained")

def approvePermissions(url, driver):

    '''
    Main logic behind approving permissions for therapist to access patient records

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    driver.get(url + "Patient/My-Therapists")
    driver.find_element_by_id('BodyContent_GridViewTherapist_LinkButtonViewPermission_0').click()
    time.sleep(10)
    driver.find_element_by_id('BodyContent_buttonPermissionApprove').click()
    logoutScript = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(logoutScript)
    driver.close()
    driver.quit()
    print(" -Patient approved permission for therapist")

def addDiagnosis(url, driver):

    '''
    Main logic behind addition of diagnosis for patient

    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    patientCredentials = getPatientCredentials()
    therapistCredentials = getTherapistCredentials()
    driver.get(url + "Therapist/My-Patients/View")
    driver.find_element_by_id('BodyContent_TextboxSearch').send_keys(patientCredentials[0])
    driver.find_element_by_id('BodyContent_ButtonSearch').click()
    time.sleep(10)
    driver.find_element_by_id('BodyContent_GridViewPatient_LinkButtonViewDiagnosis_0').click()
    time.sleep(10)
    driver.find_element_by_id('BodyContent_TextboxSearchDiagnosis').send_keys(therapistCredentials[2])
    driver.find_element_by_id('BodyContent_ButtonSearchDiagnosis').click()
    time.sleep(10)
    addDiagnosisScript = "__doPostBack('ctl00$BodyContent$GridViewPatientDiagnosisAdd$ctl02$ctl00','')"
    driver.execute_script(addDiagnosisScript)
    time.sleep(10)
    logoutScript = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(logoutScript)
    driver.close()
    driver.quit()
    print(" -Therapist has created a new diagnosis")

def viewDiagnosis(url, driver):

    '''
    Main logic behind view diagnosis for patients
    Arguments:
        url(str): Target URL
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    driver.get(url + "Patient/My-Diagnoses")
    logoutScript = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(logoutScript)
    driver.close()
    driver.quit()
    print(" -Patient is now viewing diagnosis")
