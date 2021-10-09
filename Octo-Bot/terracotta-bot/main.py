import time
import random
import numpy as np
import pyautogui
import bezier

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


workflowList = [];


def slow_type(element, pageInput):
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        element.send_keys(letter)

# bezier curve movement to element
def move_cursor_to_element(element, driver): ##move mouse to middle of element
    # need to check scroll to subtract from element location as offset
    scrollX = driver.execute_script('return window.pageXOffset;')
    scrollY = driver.execute_script('return window.pageYOffset;')
    panelHeight = driver.execute_script('return window.outerHeight - window.innerHeight;')
    x, relY = element.location["x"] - scrollX, element.location["y"] - scrollY
    absY = relY + panelHeight
    w, h = element.size["width"], element.size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to creat perfect curve
    control2 = control2X, y2


    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.02  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y, _pause=False)  # Move to point in curve
        # pyautogui.sleep(delay)  # Wait delay
        pyautogui.sleep(np.abs(np.random.normal(0.0472, 0.003)))

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
        time.sleep(np.abs(np.random.normal(0.015, 0.003)))

def resting_mouse(driver): #move mouse to right of screen

    start = pyautogui.position()

    # make ending position based on screen size
    # note that driver is made to maximise wondow so will be assumed to be same as screen size
    screen_width, screen_height = pyautogui.size()

    end = random.randint(int(screen_width*0.75), int(screen_width*0.95)), random.randint(int(screen_height*0.6),int(screen_height*0.9))
    # end = driver.execute_script("return window.innerWidth")

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control2X = (end[0] + x2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to create perfect curve
    control2 = control2X, y2 ## using y2 for both to get a more linear curve

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.02  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y, _pause=False)  # Move to point in curve
        # pyautogui.sleep(delay)  # Wait delay
        pyautogui.sleep(np.abs(np.random.normal(0.015, 0.003)))
    time.sleep(2)


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
    # relocate username box
    # username_box = driver.find_element_by_id('registerUsername')
    move_cursor_to_element(username_box, driver)
    # username_box.send_keys(username)
    slow_type(username_box, username)

    password_box = driver.find_element_by_id('registerPassword')
    move_cursor_to_element(password_box, driver)
    slow_type(password_box, password)

    name_box = driver.find_element_by_id('registerName')
    move_cursor_to_element(name_box, driver)
    slow_type(name_box, name)

    email_box = driver.find_element_by_id('registerEmail')
    move_cursor_to_element(email_box, driver)
    slow_type(email_box, email)

    register_button = driver.find_element_by_name('register')
    move_cursor_to_element(register_button, driver)
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
    loginButton = driver.find_element_by_link_text("LOGOUT")
    go_to_element(loginButton, driver)
    loginButton.click()

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

# run through all workflow functions
for i in range(len(workflowList)):
    workflowList[i](driver)
    time.sleep(2)

resting_mouse(driver)
register(driver, username, oldPassword, name, email)
resting_mouse(driver)
changePassword(driver, oldPassword, newPassword)
time.sleep(3)
resting_mouse(driver)
logout(driver)
time.sleep(3)
login(driver, username, newPassword)
time.sleep(3)

driver.quit()

print("Shutting down bot")