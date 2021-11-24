import time
import os
import random
import numpy as np
import pyautogui
import bezier
import Xlib.display
from random import randint

pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
print("pyautogui can connect")

def slow_type(element, pageInput):

    '''
    Main Logic behind typing input string by character with random interval
    
    Arguments:
        element(obj) : Input box to be typed into
        pageInput(str) : Input string to be typed
    
    Returns:
        None
    '''
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        element.send_keys(letter)

def move_cursor_to_element(element, driver): ##move mouse to middle of element
    
    '''
    Main Logic behind moving cursor to element in a bezier curve
    
    Arguments:
        element(obj) : Target element which cursor is to be moved to
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''

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

    '''
    Main Logic behind scrolling element into view with random scroll movements
    
    Arguments:
        element(obj) : Target element which has to be scrolled into view
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
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

def resting_mouse(): #move mouse to right of screen

    '''
    Main Logic behind moving cursor to random bottom-right location
    
    Arguments:
        None
    
    Returns:
        None
    '''
    start = pyautogui.position()

    # make ending position based on screen size
    # note that driver is made to maximise wondow so will be assumed to be same as screen size
    screen_width, screen_height = pyautogui.size()

    end = random.randint(int(screen_width*0.75), int(screen_width*0.95)), random.randint(int(screen_height*0.6),int(screen_height*0.9))

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



def reading_delay(driver):

    '''
    Main Logic behind adding delay based on number of words on a page
    
    Arguments:
        driver(obj): Firefox webdriver instance in python 
    
    Returns:
        None
    '''
    num_words = 0
    list_strings = driver.find_element_by_xpath("/html/body").text # extract all text on page
    for string in list_strings:
        num_words += 1 + string.count(' ') # 1 initial and 1 for each add space
    
    # Reading rate from How many words do we read per minute? A review and meta-analysis of reading rate by Marc Brysbaert
    reading_rate = np.abs(np.random.normal(238, 51.2))
    delay = (reading_rate*60)/num_words
    print("Delay by: " + str(delay) + "s")
    time.sleep(delay)



def register(driver, username, password, name, email):

    '''
    Main Logic behind registering a user account
    
    Arguments:
        driver(obj): Firefox webdriver instance in python 
        username(str) : username for account creation 
        password(str) : password for account creation 
        name(str) : name for account creation 
        email(str) : email for account creation 
    
    Returns:
        None
    '''
    resting_mouse()
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

    time.sleep(2)

def login(driver, username, password):

    '''
    Main Logic behind registering a user account
    
    Arguments:
        driver(obj): Firefox webdriver instance in python 
        username(str) : username of existing account 
        password(str) : password of existing account 
    
    Returns:
        None
    '''
    resting_mouse()
    # input username, password into respective fields and click login button
    username_box = driver.find_element_by_id('username')
    # username_box.send_keys(username)
    go_to_element(username_box, driver)
    move_cursor_to_element(username_box, driver)
    slow_type(username_box, username)

    password_box = driver.find_element_by_id('password')
    move_cursor_to_element(password_box, driver)
    slow_type(password_box, password)
    

    login_button = driver.find_element_by_name('login')
    go_to_element(login_button, driver)
    move_cursor_to_element(login_button, driver)
    login_button.click()
    time.sleep(2)

def changePassword(driver, newPassword):

    '''
    Main Logic behind registering a user account
    
    Arguments:
        driver(obj): Firefox webdriver instance in python 
        newPassword(str) : new password to be changed to 
    
    Returns:
        None
    '''
    resting_mouse()
    # input old password and new password and click change password button
    oldPassword_box = driver.find_element_by_id('changePassword')
    go_to_element(oldPassword_box, driver)
    move_cursor_to_element(oldPassword_box, driver)
    slow_type(oldPassword_box, newPassword)

    newPassword_box = driver.find_element_by_id('verifyPassword')
    move_cursor_to_element(newPassword_box, driver)
    slow_type(newPassword_box, newPassword)

    change_password_button = driver.find_element_by_name('change')
    move_cursor_to_element(change_password_button, driver)
    change_password_button.click()
    time.sleep(2)
    
    # check that "Password Updated!" text is displayed
    
    # try:
    #     passwordChange = driver.find_element_by_link_text("Password Updated!")
    #     print("Password changed")
    # except NoSuchElementException:
    #     print("Error changing password")

def logout(driver):

    '''
    Main Logic behind logging user out of a logged-in session
    
    Arguments:
        
    Returns:
        None
    '''
    print("before resting mouse")
    resting_mouse()
    # click on logout button
    print("after resting; finding logout")
    logout_button = driver.find_element_by_link_text("LOGOUT")
    print("found logout")
    print("after go to element")
    move_cursor_to_element(logout_button, driver)
    logout_button.click()
    time.sleep(2)


def getAccountNumber(driver):
    return driver.find_element_by_css_selector('[id^=accountNumber]').text

def getAccountBalance(driver):
    return driver.find_element_by_css_selector('[id^=accountBalance]').text

def verifyUpdatedBalance(oldBalance, amount):
    newBalance = getAccountBalance
    print((oldBalance + amount == newBalance))

def deposit(driver, accountNumber, amount):
    accountNumber_box = driver.find_element_by_id('depositAccountNumber')
    go_to_element(accountNumber_box, driver)
    move_cursor_to_element(accountNumber_box, driver)
    slow_type(accountNumber_box, accountNumber)

    checkNumber_box = driver.find_element_by_id('depositCheckNumber')
    go_to_element(checkNumber_box, driver)
    move_cursor_to_element(checkNumber_box, driver)
    slow_type(checkNumber_box, str(randint(10000000, 99999999)))

    amount_box = driver.find_element_by_id('depositAmount')
    go_to_element(amount_box, driver)
    move_cursor_to_element(amount_box, driver)
    slow_type(amount_box, str(amount))

    deposit_button = driver.find_element_by_name('deposit')
    go_to_element(deposit_button, driver)
    move_cursor_to_element(deposit_button, driver)
    deposit_button.click()

def transfer(driver, accountNumber, amount):
    accountNumber_box = driver.find_element_by_id('toAccountNumber')
    go_to_element(accountNumber_box, driver)
    move_cursor_to_element(accountNumber_box, driver)
    slow_type(accountNumber_box, accountNumber)

    amount_box = driver.find_element_by_id('transferAmount')
    go_to_element(amount_box, driver)
    move_cursor_to_element(amount_box, driver)
    slow_type(amount_box, str(amount))

    deposit_button = driver.find_element_by_name('transfer')
    go_to_element(deposit_button, driver)
    move_cursor_to_element(deposit_button, driver)
    deposit_button.click()



def depositFromAToB(driver, usernameA, passwordA, usernameB, passwordB, amount):

    '''
    Main Logic behind workflow to deposit funds into account
    
    Arguments:
        driver(obj): Firefox webdriver instance in python
        username(str) : username of account for funds  
        password(str) : password of account to deposit money into 
        amount(str) : amount to be deposited into account 
        
    Returns:
        None
    '''
    print("login")
    login(driver, usernameB, passwordB)

    accountNumberB = getAccountNumber(driver)
    accountBalanceB = getAccountBalance(driver)
    print("NumberB: " + accountNumberB)
    print("BalanceB: " + accountBalanceB)

    print("logout")
    logout(driver)

    print("login")
    login(driver, usernameA, passwordA)

    print("deposit")
    deposit(driver, accountNumberB, amount)

    print("logout")
    logout(driver)

    print("login")
    login(driver, usernameB, passwordB)

    print("logout")
    logout(driver)

def transferFromAToB(driver, usernameA, passwordA, usernameB, passwordB, amount):

    '''
    Main Logic behind workflow to deposit funds into account
    
    Arguments:
        driver(obj): Firefox webdriver instance in python
        username(str) : username of account for funds  
        password(str) : password of account to deposit money into 
        amount(str) : amount to be deposited into account 
        
    Returns:
        None
    '''

    print("login B")
    login(driver, usernameB, passwordB)

    accountNumberB = getAccountNumber(driver)
    accountBalanceB = getAccountBalance(driver)
    print("NumberB: " + accountNumberB)
    print("BalanceB: " + accountBalanceB)

    print("logout B")
    logout(driver)

    print("login A")
    login(driver, usernameA, passwordA)

    print("transfer A to B")
    transfer(driver, accountNumberB, amount)

    print("logout A")
    logout(driver)

    print("login B")
    login(driver, usernameB, passwordB)

    print("logout B")
    logout(driver)

def depositTransferParentToAToB(driver, usernameParent, passwordParent, usernameA, passwordA, usernameB, passwordB, amountDeposit, amountTransfer):

    '''
    Main Logic behind workflow to deposit funds from Parent to A and transfer from A to B
    
    Arguments:
        driver(obj): Firefox webdriver instance in python
        username(str) : username of account for funds  
        password(str) : password of account to deposit money into 
        amount(str) : amount to be deposited into account 
        
    Returns:
        None
    '''

    print("login A")
    login(driver, usernameA, passwordA)

    accountNumberA = getAccountNumber(driver)
    accountBalanceA = getAccountBalance(driver)
    print("NumberA: " + accountNumberA)
    print("BalanceA: " + accountBalanceA)

    print("logout A")
    logout(driver)

    print("login parent")
    login(driver, usernameParent, passwordParent)

    print("deposit parent to A")
    deposit(driver, accountNumberA, amountDeposit)

    print("logout parent")
    logout(driver)

    print("login A")
    login(driver, usernameA, passwordA)

    print("logout A")
    logout(driver)

    print("login B")
    login(driver, usernameB, passwordB)

    accountNumberB = getAccountNumber(driver)
    accountBalanceB = getAccountBalance(driver)
    print("NumberB: " + accountNumberB)
    print("BalanceB: " + accountBalanceB)


    print("logout B")
    logout(driver)

    print("login A")
    login(driver, usernameA, passwordA)

    print("transfer A to B")
    transfer(driver, accountNumberB, amountTransfer)

    print("logout A")
    logout(driver)

    print("login B")
    login(driver, usernameB, passwordB)

    print("logout B")
    logout(driver)

