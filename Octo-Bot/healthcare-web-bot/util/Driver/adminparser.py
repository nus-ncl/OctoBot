import codecs
import csv
import json
import os
import random
import sys

directory = str(os.getcwd())

final_data = {"url": "http://10.10.0.112"}

def getNumberRecords():

    '''
    Counts the number of username-password for admin.csv file

    Arguments:
        None
    
    Returns:
        number of username-password records in admin.csv file
    '''

    fileDirectory = directory + "/config/admin.csv"
    readFile=csv.reader(codecs.open(fileDirectory, encoding='utf-8'),delimiter=",")
    number = 0
    for x in readFile:
        number += 1
    return number

def checkFilesExist(botNumber):

    '''
    Checks if the csv files to be generated already exist

    Arguments:
        botNumber (int): Number of admin bot concurrently running
    
    Returns:
        True, if the files already exist. Else, False

    '''
    fileNumber = botNumber + 20
    number = 0
    while (number <= fileNumber):
        outputFileDirectory = directory + "/config/admin/adminLogin" + str(number) + ".csv"
        if os.path.exists(outputFileDirectory):
            number += 1
            continue
        else:
            return False
    return True

def genAdminFiles(botNumbers):
    
    '''
    Generate csv files for different usernames-passwords according to the number of bots

    Arguments: 
        botNumber (int): Number of admin bot concurrently running

    Returns:
        None

    '''
    fileNumber = botNumbers + 20
    recordsPerFile = (int)(getNumberRecords()/fileNumber)
    print(recordsPerFile)
    adminFileDirectory = directory + "/config/admin.csv"
    readFile=csv.reader(codecs.open(adminFileDirectory, encoding='utf-8'),delimiter=",")
    number = 0
    for row in readFile:
        outputFileDirectory = directory + "/config/admin/adminLogin" + str(number) + ".csv"
        writeFile = open(outputFileDirectory,mode = 'a', newline = '')
        writer = csv.writer(writeFile, delimiter = ',')
        writer.writerow(row)
        if (number >= fileNumber):
            number = 0
        number += 1

def getCredentials(botNumbers):
    '''

    Obtain credentials for the bot to login

    Arguments:
        botNumber (int): Number of admin bot concurrently running
    
    Returns:
        None
    '''
    trackNumber = 0
    newRecords = []
    credentials = []
    number = ((random.randint(1,2000)%23) * (random.randint(1,2000)%17) * (random.randint(1000,2000)%13)) % (botNumbers + 20)
    fileDirectory = directory + "/config/admin/adminLogin" + str(number) + ".csv"
    print("Reading from " + str(fileDirectory))
    readFile=csv.reader(codecs.open(fileDirectory, encoding='utf-8'),delimiter=",")
    for rows in readFile:
        if (trackNumber == 0):
            credentials.append(rows[0])
            credentials.append(rows[1])
            trackNumber += 1
        else:
            newRecords.append(rows)
    credentials.append(number)
    writeFile = open(fileDirectory,mode = 'w', newline = '')
    for record in newRecords:
        writeFile.write(record[0] + ',' + record[1])
        writeFile.write('\n')
    return credentials

def writeBack(username, password, fileNumber):
    '''

    Writes back the credentials to the csv file after all admin actions have been completed

    Arguments:
        username (str): Username that the bot is logging in with
        password (str): Password that the bot is logging in with
        fileNumber (int): file number for the csv file that the bot is going to open to read the credentials
    
    Returns:
        None
    '''
    fileDirectory = directory + "/config/admin/adminLogin" + str(fileNumber) + ".csv"
    writeFile = open(fileDirectory,mode = 'a', newline = '')
    writer = csv.writer(writeFile, delimiter = ',')
    writeBack = []
    writeBack.append(username)
    writeBack.append(password)
    writer.writerow(writeBack)
    
def getUrl():
    '''
    Obtain the url that the bot is logging into
    
    Arguments:
        None
    
    Returns:
        None
    '''
    return "https://10.10.0.112"
