import time 

def login(driver, username, password):

    '''
    Main logic behind the logging in of accounts executed by the bot

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        None
    '''
    print("Logging in...")
    username_box = driver.find_element_by_id('BodyContent_inputNRIC')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('BodyContent_inputPassword')
    password_box.send_keys(password)
    driver.find_element_by_id('BodyContent_ButtonLogin').click()
    time.sleep(3)
    time.sleep(10)
    if (str(driver.current_url) != "https://10.10.0.112/Role-Selection"):
        print("Multi-selection role enabled!")
    else:
        print("Logged in!")

def logout(driver):
    '''
    Main Logic behind logging out of user account

    Arguments:
        driver(obj): firefox webdriver instance in python
    
    Returns:
        None
    '''
    script = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(script)
    
