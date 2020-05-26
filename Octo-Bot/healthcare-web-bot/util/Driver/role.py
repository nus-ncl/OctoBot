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

def getRole(driver):
    print("User privileges:")
    if (isAdmin(driver)):
        print(" -Admin")
    if (isResearcher(driver)):
        print(" -Researcher")
    if (isTherapist(driver)):
        print(" -Therapist")
    if (isPatient(driver)):
        print(" -Patient")
