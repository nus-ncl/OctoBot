
MIN_IN_SECS = 60
HOUR_IN_SECS = 3600
DAY_IN_SECS = 86400

def timeStr2Secs(timeStr):
    '''
    Converts at timeStr string in the format (DD:HH:MM:SS) into seconds.

    Arguments:
        timeStr (str): timeStr string in the format (DD:HH:MM:SS)
    
    Returns:
        totalSecs (int): timeStr string in seconds.
    '''

    totalSecs = 0

    timeStrings = timeStr.split(':')
    timeStrings.reverse()


    noOfValues = len(timeStrings)

    if noOfValues >= 1 and timeStrings[0].isnumeric(): # seconds
        totalSecs += abs(int(timeStrings[0]))
    if noOfValues >= 2 and timeStrings[1].isnumeric(): # mins
        totalSecs += abs(int(timeStrings[1])) * MIN_IN_SECS
    if noOfValues >= 3 and timeStrings[2].isnumeric(): # hours
        totalSecs += abs(int(timeStrings[2])) * HOUR_IN_SECS
    if noOfValues >= 4 and timeStrings[3].isnumeric(): # days
        totalSecs += abs(int(timeStrings[3])) * DAY_IN_SECS

    return totalSecs
