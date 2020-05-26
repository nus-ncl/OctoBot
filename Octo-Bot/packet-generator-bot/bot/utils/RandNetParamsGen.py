import random

def GetRandomIpInRange(IpList):
    assert type(IpList) == tuple or type(IpList) == list, 'IpList is a %s not a list or tuple' %type(IpList)
    return IpList[random.randint(0,len(IpList))]
    

def GenerateRandomIp():
    oct1 = random.randint(1,255)
    oct2 = random.randint(0,255)
    oct3 = random.randint(0,255)
    oct4 = random.randint(1,255)

    return '%i.%i.%i.%i' %(oct1,oct2,oct3,oct4)
def GenerateRandomIpv6():
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

def RandomRawData(size=200):
    data = ''
    for i in range(size):
        data += chr(random.randint(0,127))
    return data
             

def RandomSafePortGenerator():
    return random.randint(49152,65535)

def RandomSafeSeqGenerator():
    return random.randint(1,3000000000)