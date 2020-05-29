from scapy.utils import rdpcap
from os import path


def openPcap(pcapFile):
    '''
    Opens a capture file if it exists. 

    Arguments:
        pcapFile (str): path to capture file
    
    Returns:
        List: list of packets if the capture exists else returns None
    '''
    if path.exists(pcapFile):
        return rdpcap(pcapFile)
    else:
        return None