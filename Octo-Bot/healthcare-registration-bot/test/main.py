import argparse
from BotActions import (addDiagnosis, adminLogin, approvePermissions,
                        assignTherapist, createNewRecord, getDriver,
                        patientLogin, registerPatientAccount,
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
    print("Registration bot starting up in 5...")
    print("Registration bot starting up in 4...")
    print("Registration bot starting up in 3...")
    print("Registration bot starting up in 2...")
    print("Registration bot starting up in 1...")
    main(url)
    print("Registration bot completed and closing down in 5...")
    print("Registration bot completed and closing down in 4...")
    print("Registration bot completed and closing down in 3...")
    print("Registration bot completed and closing down in 2...")
    print("Registration bot completed and closing down in 1...")
