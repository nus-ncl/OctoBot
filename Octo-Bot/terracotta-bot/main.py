import time

from Actions import (register, resting_mouse, changePassword, logout, login)

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pyvirtualdisplay import Display 

workflowList = [];

DISPLAY_VISIBLE = 1
DISPLAY_WIDTH = 2400
DISPLAY_HEIGHT = 1000


# start display 
display = Display(visible=DISPLAY_VISIBLE, size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))
display.start()

def getDriver():

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
    # firefox_options.add_argument("--headless")
    # firefox_options.add_argument("--no-sandbox")
    # firefox_options.add_argument("--disable-dev-shm-usage")
    # firefox_options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(firefox_options = firefox_options,firefox_profile = profile)
    # driver.get(url)
    return driver

url = "http://localhost:8080/"
username = "test-1"
oldPassword = "Oldpassword@1"
name = "Test 1"
email = "test1@test.com"
newPassword = "NewPassword@1"

print("Starting up bot")  
driver = getDriver()

driver.get(url)

#maximise browser window
driver.maximize_window()
# driver.set_window_size(2300, 900)

# run through all workflow functions
for i in range(len(workflowList)):
    workflowList[i](driver)
    time.sleep(2)


register(driver, username, oldPassword, name, email)
changePassword(driver, oldPassword, newPassword)
logout(driver)
login(driver, username, newPassword)
driver.quit()

display.stop()
print("Shutting down bot")