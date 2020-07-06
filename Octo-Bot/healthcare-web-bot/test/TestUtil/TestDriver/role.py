
def isAdmin(driver):

    '''
    Checks if the defined credentials has an admin role 

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        True if the credentials has an admin role. Else, False
    '''
    try:
        driver.find_element_by_id('BodyContent_buttonLoginAdmin')
        return True
    except:
        return False

def isPatient(driver):

    '''
    Checks if the defined credentials has a patient role 

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        True if the credentials has an patient role. Else, False
    '''
    try:
        driver.find_element_by_id('BodyContent_buttonLoginPatient')
        return True
    except:
        return False

def isResearcher(driver):

    '''
    Checks if the defined credentials has a researcher role 

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        True if the credentials has an researcher role. Else, False
    '''
    try:
        driver.find_element_by_id('BodyContent_buttonLoginResearcher')
        return True
    except:
        return False

def isTherapist(driver):

    '''
    Checks if the defined credentials has a therapist role 

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        True if the credentials has an therapist role. Else, False
    '''
    try:
        driver.find_element_by_id('BodyContent_buttonLoginTherapist')
        return True
    except:
        return False
