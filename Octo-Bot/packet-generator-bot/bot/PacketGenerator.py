import time

from scapy.all import *


class PacketGenerator():

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
                    print ('Iteration #%i' % i)
                    print ('sending %i packets a sec...' % send_rate)
                    sendp(self.packets,iface=self.interface)
                    if self.delay > 0:
                        print ("pausing for %i secs... " % self.delay)
                        time.sleep(self.delay)
        elif self.time is not None: # time indicated, loops ignored
            timestart = time.time()
            timeend = timestart + self.time
            i = 1
            while time.time() < timeend:
                print ('Iteration #%i' % i)
                sendp(self.packets,iface=self.interface)
                print ('stopping in %3f secs' % max((timeend - time.time(), 0)))
                if self.delay > 0:
                    print ("pausing for %3f secs... " % self.delay)
                    time.sleep(self.delay)
                print("")
                i += 1



