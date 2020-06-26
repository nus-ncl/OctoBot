import codecs
import csv
import json
import os
import random
import sys

directory = str(os.getcwd()) + "//config"

def getAdminCredentials():

    '''
    Obtains necessary information for admin role

    Arguments:
        None

    Returns:
        Dictionary object of all the necessary information that the admin requires
    '''
    fileName = directory + "//admin.csv"
    readFile=csv.reader(codecs.open(fileName, encoding='utf-8'),delimiter=",")
    credentials = []
    for row in readFile:
        for x in row:
            if (x == ""):
                continue
            else:
                credentials.append(x)
    return credentials

def getTherapistCredentials():

    '''
    Obtains necessary information for therapist role

    Arguments:
        None

    Returns:
        Dictionary object of all the necessary information that the therapist requires
    '''
    fileName = directory + "//therapist.csv"
    readFile=csv.reader(codecs.open(fileName, encoding='utf-8'),delimiter=",")
    credentials = []
    for row in readFile:
        for x in row:
            if (x == ""):
                continue
            else:
                credentials.append(x)
    return credentials

def getPatientCredentials():

    '''
    Obtains necessary information for patient role

    Arguments:
        None

    Returns:
        Dictionary object of all the necessary information that the patient requires
    '''
    fileName = directory + "//patient.csv"
    readFile=csv.reader(codecs.open(fileName, encoding='utf-8'),delimiter=",")
    credentials = []
    for row in readFile:
        for x in row:
            if (x == ""):
                continue
            else:
                credentials.append(x)
    return credentials
