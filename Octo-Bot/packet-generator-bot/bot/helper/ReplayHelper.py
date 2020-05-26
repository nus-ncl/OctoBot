from scapy.utils import rdpcap
from os import path


def openPcap(pcapFile):
    if path.exists(pcapFile):
        return rdpcap(pcapFile)
    else:
        return None