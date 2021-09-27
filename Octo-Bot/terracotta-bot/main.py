import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    username_box.send_keys(username)

    password_box = driver.find_element_by_id('registerPassword')
    password_box.send_keys(password)

    name_box = driver.find_element_by_id('registerName')
    name_box.send_keys(name)

    email_box = driver.find_element_by_id('registerEmail')
    email_box.send_keys(email)

    driver.find_element_by_name('register').click()

    time.sleep(3)

# def login(driver, username, password):
#     # input username, password into respective fields and click login button
#     username_box = driver.find_element_by_id('username')
#     username_box.send_keys(username)

#     password_box = driver.find_element_by_id('password')
#     password_box.send_keys(password)

def changePassword(driver, oldPassword, newPassword):
    # input old password and new password and click change password button
    oldPassword_box = driver.find_element_by_id('changePassword')
    oldPassword_box.send_keys(newPassword)

    newPassword_box = driver.find_element_by_id('verifyPassword')
    newPassword_box.send_keys(newPassword)

    driver.find_element_by_name('change').click()
    time.sleep(3)
    # check that "Password Updated!" text is displayed
    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.xpath, "//*[text()='Password Updated!']"))
    #     )
    #     print("Password changed")
    # except:
    #     driver.quit()
    #     print("Error changing password")

# def logout(driver):
#     # click on logout button

url = "http://localhost:8080/"
username = "test-1"
oldPassword = "Oldpassword@1"
name = "Test 1"
email = "test1@test.com"
newPassword = "NewPassword@1"

print("Starting up bot")  
driver = getDriver()

driver.get(url)
register(driver, username, oldPassword, name, email)
changePassword(driver, oldPassword, newPassword)
# logout(driver)
# login(driver, username, password)

driver.quit()

print("Shutting down bot")