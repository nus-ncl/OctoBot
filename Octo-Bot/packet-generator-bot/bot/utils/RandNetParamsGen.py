import random

def GetRandomIpInRange(IpList):
    '''
    Picks a random IP in IpList

    Arguments:
        IpList (List): list of IPs
    
    Returns:
        str: random IP in IpList
    '''

    assert type(IpList) == tuple or type(IpList) == list, 'IpList is a %s not a list or tuple' %type(IpList)
    return IpList[random.randint(0,len(IpList))]
    
def GenerateRandomIp():
    '''
    Generates a random IPv4 address.

    Arguments:
        None
    
    Returns:
        str: random IPv4 address
    '''

    oct1 = random.randint(1,255)
    oct2 = random.randint(0,255)
    oct3 = random.randint(0,255)
    oct4 = random.randint(1,255)

    return '%i.%i.%i.%i' %(oct1,oct2,oct3,oct4)

def GenerateRandomIpv6():
    '''
    Generates a random IPv6 address.

    Arguments:
        None
    
    Returns:
        str: random IPv6 address
    '''

    Value1 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value2 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value3 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value4 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value5 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value6 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value7 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    Value8 = ''.join([random.choice('0123456789abcdef') for i in range(4)
                    ])
    
    return '%s:%s:%s:%s:%s:%s:%s:%s'  %(Value1,
                                        Value2,
                                        Value3,
                                        Value4,
                                        Value5,
                                        Value6,
                                        Value7,
                                        Value8)                  
                    
def GenerateRandomMac():
    '''
    Generates a random IPv6 address.

    Arguments:
        None
    
    Returns:
        str: random IPv6 address
    '''

    Value1 = random.choice('0123456789ABCDEF') + random.choice('26AE')
    Value2 = ''.join([random.choice('0123456789ABCDEF') for i in range(2)])
    Value3 = ''.join([random.choice('0123456789ABCDEF') for i in range(2)])
    Value4 =''.join([random.choice('0123456789ABCDEF') for i in range(2)]) 
    Value5 = ''.join([random.choice('0123456789ABCDEF') for i in range(2)])
    Value6 = ''.join([random.choice('0123456789ABCDEF') for i in range(2)])
    return '%s:%s:%s:%s:%s:%s' %(Value1,
                                 Value2,
                                 Value3,
                                 Value4,
                                 Value5,
                                 Value6)

def GenerateRandomRawData(size=200):
    '''
    Generates random raw data.

    Arguments:
        None
    
    Returns:
        str: random data of size (size)
    '''

    data = ''
    for i in range(size):
        data += chr(random.randint(0,127))
    return data
             
def GenerateRandomSafePort():
    '''
    Generates a random safe port number.

    Arguments:
        None
    
    Returns:
        int: random safe port number
    '''
    
    return random.randint(49152,65535)

def GenerateRandomSafeSeq():
    '''
    Generates a random secure sequence number.

    Arguments:
        None
    
    Returns:
        int: random secure sequence number
    '''

    return random.randint(1,3000000000)