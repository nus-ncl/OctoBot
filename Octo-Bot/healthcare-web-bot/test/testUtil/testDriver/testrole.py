""" Checks the role of the user
isAdmin function checks if the user is an admin
isPatient function checks if the user is a patient
isResearcher function checks if the user is a reasearcher
isTherapist function checks if the user is a researcher
"""

def isAdmin(driver):
    try:
        driver.find_element_by_id('BodyContent_buttonLoginAdmin')
        return True
    except:
        return False

def isPatient(driver):
    try:
        driver.find_element_by_id('BodyContent_buttonLoginPatient')
        return True
    except:
        return False

def isResearcher(driver):
    try:
        driver.find_element_by_id('BodyContent_buttonLoginResearcher')
        return True
    except:
        return False

def isTherapist(driver):
    try:
        driver.find_element_by_id('BodyContent_buttonLoginTherapist')
        return True
    except:
        return False
