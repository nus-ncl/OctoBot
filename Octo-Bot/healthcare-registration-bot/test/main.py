import argparse

from BotActions import (addDiagnosis, adminLogin, approvePermissions,
                        assignTherapist, createNewRecord, getDriver,
                        getDriverStatus, patientLogin, registerPatientAccount,
                        requestPermissions, therapistLogin, viewDiagnosis)
from FileParser import (getAdminCredentials, getPatientCredentials,
                        getTherapistCredentials)


def main(url):
    '''
    Logic behind the main function

    Arguments:
        url(str) : Target URL

    Returns:
        None
    '''
    driver = None
    try:
        adminCredentials = getAdminCredentials()
        therapistCredentials = getTherapistCredentials()
        patientCredentials = getPatientCredentials()
        driver = getDriver(url)
        adminLogin(url, driver, adminCredentials[0], adminCredentials[1])
        registerPatientAccount(url, driver)
        assignTherapist(url, driver)
        driver = getDriver(url)
        patientLogin(url, driver, patientCredentials[0], patientCredentials[8])
        createNewRecord(url, driver)
        driver = getDriver(url)
        therapistLogin(url, driver, therapistCredentials[0], therapistCredentials[1])
        requestPermissions(url, driver)
        driver = getDriver(url)
        patientLogin(url, driver, patientCredentials[0], patientCredentials[8])
        approvePermissions(url, driver)
        driver = getDriver(url)
        therapistLogin(url, driver, therapistCredentials[0], therapistCredentials[1])
        addDiagnosis(url, driver)
        driver = getDriver(url)
        patientLogin(url, driver, patientCredentials[0], patientCredentials[8])
        viewDiagnosis(url, driver)
    except:
        if (getDriverStatus(driver) == "alive"):
            driver.quit()
            print("Invalid hostname. Please try again!")
        else:
            print("Invalid hostname. Please try again!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
        "Arguments for program")
    parser.add_argument('-u', metavar = 'hostname', type=str, \
        help='URL of the website that the bot is using', default = "https://10.10.0.112/")
    args = parser.parse_args()
    url = args.u
    urlPrintLine = "Preparing to access from " + str(url) + "..."
    print(urlPrintLine)
    print("Starting up registration bot...")
    main(url)
    print("Closing down registration bot...")
