import os
import codecs
import csv
import random

directory = str(os.getcwd())

def therapistGetNumberRecords():

    '''
    Obtains the number of username-password from therapist.csv

    Arguments:
        None
    
    Returns:
        None
    '''
    fileDirectory = directory + "/config/therapist.csv"
    readFile=csv.reader(codecs.open(fileDirectory, encoding='utf-8'),delimiter=",")
    number = 0
    for x in readFile:
        number += 1
    return number

def therapistCheckFilesExist(botNumber):

    '''
    Checks if the csv files already exist before the bot starts generating new csv files

    Arguments:
        botNumber(int) : The number of therapist bots concurrently running
    
    Returns:
        True if the csv files do not exist. Else, False
    '''
    fileNumber = botNumber + 20
    number = 0
    while (number <= fileNumber):
        outputFileDirectory = directory + "/config/therapist/therapistLogin" + str(number) + ".csv"
        if os.path.exists(outputFileDirectory):
            number += 1
            continue
        else:
            return False
    return True

def genTherapistFiles(botNumbers):

    '''
    Generates the therapist csv files from therapist.csv, according to the number of bots

    Arguments:
        botNumber(int) : The number of therapist bots concurrently running
    
    Returns:
        None
    '''
    fileNumber = botNumbers + 20
    recordsPerFile = (int)(therapistGetNumberRecords()/fileNumber)
    print(recordsPerFile)
    adminFileDirectory = directory + "/config/therapist.csv"
    readFile=csv.reader(codecs.open(adminFileDirectory, encoding='utf-8'),delimiter=",")
    number = 0
    for row in readFile:
        outputFileDirectory = directory + "/config/therapist/therapistLogin" + str(number) + ".csv"
        writeFile = open(outputFileDirectory,mode = 'a', newline = '')
        writer = csv.writer(writeFile, delimiter = ',')
        writer.writerow(row)
        if (number >= fileNumber):
            number = 0
        number += 1

def therapistGetCredentials(botNumbers):

    '''
    Obtains credentials for the bots running therapist role

    Arguments:
        botNumber(int) : The number of therapist bots concurrently running
    
    Returns:
        None
    '''
    trackNumber = 0
    newRecords = []
    credentials = []
    number = ((random.randint(1,2000)%23) * (random.randint(1,2000)%17) * (random.randint(1000,2000)%13)) % (botNumbers + 20)
    fileDirectory = directory + "/config/therapist/therapistLogin" + str(number) + ".csv"
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

def therapistWriteBack(username, password, fileNumber):

    '''
    Writes back the credentials into the therapist csv files that are being generated

    Arguments:
        username(str) : username that the bot is logging in with
        password(str) : password that the bot is logging in with
        fileNumber(int) : fileNumber that the bot uses to obtain the credentials
    
    Returns:
        None
    '''
    fileDirectory = directory + "/config/therapist/therapistLogin" + str(fileNumber) + ".csv"
    writeFile = open(fileDirectory,mode = 'a', newline = '')
    writer = csv.writer(writeFile, delimiter = ',')
    writeBack = []
    writeBack.append(username)
    writeBack.append(password)
    writer.writerow(writeBack)
    