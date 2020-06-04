import time 
from testUtil.testDriver.testRole import getRole

def login(driver, username, password):
    print("Logging in...")
    username_box = driver.find_element_by_id('BodyContent_inputNRIC')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('BodyContent_inputPassword')
    password_box.send_keys(password)
    driver.find_element_by_id('BodyContent_ButtonLogin').click()
    time.sleep(3)
    time.sleep(10)
    if (str(driver.current_url) != "https://10.10.0.112/Role-Selection"):
        print("Invalid credentials. Please try again!")
    else:
        print("Logged in!")
        getRole(driver)

def logout(driver):
    script = "__doPostBack('ctl00$ctl13','')"
    driver.execute_script(script)
    
