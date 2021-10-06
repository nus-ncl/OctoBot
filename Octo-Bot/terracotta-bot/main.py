import time
import random
import numpy as np

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


workflowList = [];


def slow_type(pageElem, pageInput):
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        pageElem.send_keys(letter)

def go_to_element(element, driver):
    window_height = driver.execute_script("return window.innerHeight")
    start_dom_top = driver.execute_script("return document.documentElement.scrollTop")
    element_location = element.location['y']
    desired_dom_top = element_location - window_height/2 #Center It!
    to_go = desired_dom_top - start_dom_top
    cur_dom_top = start_dom_top
    while np.abs(cur_dom_top - desired_dom_top) > 70:
        scroll = np.random.uniform(2,69) * np.sign(to_go)
        driver.execute_script("window.scrollBy(0, {})".format(scroll))
        cur_dom_top = driver.execute_script("return document.documentElement.scrollTop")
        time.sleep(np.abs(np.random.normal(0.0472, 0.003)))

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

def register(driver, username, password, name, email):
    # input username, password, name, email into respective fields and click register button
    username_box = driver.find_element_by_id('registerUsername')
    go_to_element(username_box, driver)
    # username_box.send_keys(username)
    slow_type(username_box, username)

    password_box = driver.find_element_by_id('registerPassword')
    slow_type(password_box, password)

    name_box = driver.find_element_by_id('registerName')
    slow_type(name_box, name)

    email_box = driver.find_element_by_id('registerEmail')
    slow_type(email_box, email)

    register_button = driver.find_element_by_name('register')
    register_button.click()

    time.sleep(3)

def login(driver, username, password):
    # input username, password into respective fields and click login button
    username_box = driver.find_element_by_id('username')
    # username_box.send_keys(username)
    go_to_element(username_box, driver)
    slow_type(username_box, username)

    password_box = driver.find_element_by_id('password')
    slow_type(password_box, password)
    

    login_button = driver.find_element_by_name('login')
    go_to_element(login_button, driver)
    login_button.click()

def changePassword(driver, oldPassword, newPassword):
    # input old password and new password and click change password button
    oldPassword_box = driver.find_element_by_id('changePassword')
    go_to_element(oldPassword_box, driver)
    slow_type(oldPassword_box, newPassword)

    newPassword_box = driver.find_element_by_id('verifyPassword')
    slow_type(newPassword_box, newPassword)

    change_password_button = driver.find_element_by_name('change')
    change_password_button.click()
    
    # check that "Password Updated!" text is displayed
    
    # try:
    #     passwordChange = driver.find_element_by_link_text("Password Updated!")
    #     print("Password changed")
    # except NoSuchElementException:
    #     print("Error changing password")

def logout(driver):
    # click on logout button
    loginButton = driver.find_element_by_link_text("LOGOUT").click()

url = "http://localhost:8080/"
username = "test-1"
oldPassword = "Oldpassword@1"
name = "Test 1"
email = "test1@test.com"
newPassword = "NewPassword@1"

print("Starting up bot")  
driver = getDriver()

driver.get(url)


# run through all workflow functions
for i in range(len(workflowList)):
    workflowList[i](driver)
    time.sleep(2)

loginButton = driver.find_element_by_link_text("LOGIN").click()
time.sleep(3)
register(driver, username, oldPassword, name, email)
changePassword(driver, oldPassword, newPassword)
time.sleep(3)
logout(driver)
time.sleep(3)
login(driver, username, newPassword)
time.sleep(3)

driver.quit()

print("Shutting down bot")