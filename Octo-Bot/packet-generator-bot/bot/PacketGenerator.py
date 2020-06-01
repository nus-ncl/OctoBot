import time

from scapy.all import *


class PacketGenerator():
    '''
    Represents a packet generator. 
    Should be instantiated by other modules to setup the type of packets to generate.

    Attributes:
        interface: network interface to use
        packets: packets to send
        ipMap: map for modifying IPs
        portMap: map for modifying port numbers
        isIPRemap: flag to trigger IP modifications
        isPortRemap: flag to trigger Port modifications
        isMacRemap: flag to trigger Mac modifications
        time: duration of generation
        loop: number of times to generate (mutually exclusive with time)
        delay: delay between each repetition
    '''

    def __init__(self):
        self.interface = None
        self.packets = []
        self.ipMap = {}
        self.portMap ={}
        self.macMap ={}
        self.isIPRemap = False
        self.isPortRemap = False
        self.isMacRemap = False
        self.time = None
        self.loop = 1
        self.delay = 0



    def setupInterface(self,
                       interface = None,
                       ):
        self.interface= interface

    def setupIPAddr(self,
                       original,
                       new):
        self.isIPRemap = True
        self.ipMap[original] = new
    
    def setupPort(self,
                         original,
                         new):
        self.isPortRemap = True
        self.portMap[original] = new
    
        
    def setupMac(self,
                 original,
                 new):
        self.isMacRemap = True
        self.macMap[original] = new

    def remapIP(self, 
                ipAddr):
        if ipAddr in self.ipMap:
            return self.ipMap[ipAddr]
        else:
            return ipAddr
    
    def remapPort(self, 
                  port):
        if port in self.portMap:
            return self.portMap[port]
        else:
            return port
    
    def remapMac(self, 
                 mac):
        if mac in self.macMap:
            return self.macMap[mac]
        else:
            return mac
            
    def sendPackets(self,
                    send_rate = None,
                    outfile = None):

        if outfile != None:
            wrpcap(outfile,self.packets)        
    
        for pkt in self.packets:
            if self.isIPRemap and pkt.haslayer(IP):
                pkt[IP].src = self.remapIP(pkt[IP].src)
                pkt[IP].dst = self.remapIP(pkt[IP].dst)
                del pkt[IP].chksum
                if pkt.haslayer(TCP):
                    del pkt[TCP].chksum
            if self.isPortRemap and pkt.haslayer(TCP):
                pkt[TCP].sport = self.remapPort(pkt[TCP].sport)
                pkt[TCP].dport = self.remapPort(pkt[TCP].dport)
                del pkt[TCP].chksum
            if self.isMacRemap and pkt.haslayer(Ether):
                pkt[Ether].src = self.remapMac(pkt[Ether].src)
                pkt[Ether].dst = self.remapMac(pkt[Ether].dst)

        if self.time is None: # No time indicated
            for i in range(1, self.loop + 1):      
                sendp(self.packets,iface=self.interface)
                if self.delay > 0:
                    time.sleep(self.delay)

        elif self.time is not None: # time indicated, loops ignored
            timestart = time.time()
            timeend = timestart + self.time
            i = 1
            while time.time() < timeend:
                sendp(self.packets,iface=self.interface)
                if self.delay > 0:
                    time.sleep(self.delay)
                i += 1



