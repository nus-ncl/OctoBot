import time
import os
import argparse


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pyvirtualdisplay import Display 

def getDriver(showDisplay):

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
    if (showDisplay != 1):
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(firefox_options = firefox_options,firefox_profile = profile)
    # driver.get(url)
    return driver



if __name__== "__main__":
    parser = argparse.ArgumentParser(description = \
        "Arguments for program")

    parser.add_argument('-url', metavar = 'url of application', type=str, \
        help='Target Website URL', default = 'http://127.0.0.1:8080/')

    parser.add_argument('-wf', metavar = 'workflow to use', type=str, \
        help='Workflow for this bot', default = 'create')

    parser.add_argument('-u', metavar = 'username', type=str, \
        help='Username to be used', default = 'test-1')

    parser.add_argument('-orgPass', metavar = 'password', type=str, \
        help='Password to be used', default = 'Oldpassword@1')

    parser.add_argument('-p', metavar = 'new password', type=str, \
        help='New password to be changed to', default = 'Password@1')

    parser.add_argument('-n', metavar = 'name of user', type=str, \
        help='Name to be used', default = 'Test 1')

    parser.add_argument('-e', metavar = 'email of user', type=str, \
        help='Email to be used', default = 'test1@test.com')

    parser.add_argument('-u2', metavar = 'username of B', type=str, \
        help='Username to be used', default = 'test-2')
    
    parser.add_argument('-p2', metavar = 'password of B', type=str, \
        help='New password to be changed to', default = 'Password@2')

    parser.add_argument('-u3', metavar = 'username of Parent', type=str, \
        help='Username to be used', default = 'test-3')

    parser.add_argument('-p3', metavar = 'password of Parent', type=str, \
        help='New password to be changed to', default = 'Password@3')

    parser.add_argument('-d', metavar = 'display', type=int, \
        help='Time to sleep between crawling of website links', default = 0)
    
    args = parser.parse_args()

    workflow = args.wf
    showDisplay = args.d
    url = args.url
    username = args.u
    oldPassword = args.orgPass
    name = args.n
    email = args.e
    password = args.p

    usernameB = args.u2
    passwordB = args.p2

    usernameParent = args.u3
    passwordParent = args.p3

    if (showDisplay != 1):

        DISPLAY_VISIBLE = 0
        DISPLAY_WIDTH = 2400
        DISPLAY_HEIGHT = 1000
        # print(os.environ['DISPLAY'])
        # start display 
        display = Display(visible=DISPLAY_VISIBLE, size=(DISPLAY_WIDTH, DISPLAY_HEIGHT), backend="xvfb", use_xauth=True)
        display.start()
        print(os.environ['DISPLAY'])

    print("Starting up bot")  
    driver = getDriver(showDisplay)



    from Actions import (reading_delay, register, changePassword, logout, login, depositFromAToB, transferFromAToB, depositTransferParentToAToB)


    driver.get(url)

    #maximise browser window
    driver.maximize_window()
    # driver.set_window_size(2300, 900)

    reading_delay(driver) # add delay for initial page reading 
    if workflow == 'create':
        register(driver, username, password, name, email)
    elif workflow == 'password':
        print("register")
        register(driver, username, oldPassword, name, email)

        print("change password")
        changePassword(driver, password)

        print("logout")
        logout(driver)

        print("login")
        login(driver, username, password)
    elif workflow == 'deposit':
        depositFromAToB(driver, username, password, usernameB, passwordB, 100.0)
    elif workflow == 'transfer':
        transferFromAToB(driver, username, password, usernameB, passwordB, 100.0)
    elif workflow == 'parentSub':
        depositTransferParentToAToB(driver, usernameParent, passwordParent, username, password, usernameB, passwordB, 100.0, 100.0)

    driver.quit()

    if (showDisplay != 1):
        display.stop()

    print("Shutting down bot")
