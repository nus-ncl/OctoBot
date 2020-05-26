from scapy.all import *

from PacketGenerator import *
from helper.ReplayHelper import *


def generateReplay(args):

    for pcapFile in args.pcap:
        # Preparing Generator
        packets = []
        packets = openPcap(pcapFile)
        assert packets is not None, "pcap file to replay must exist"
        generator = PacketGenerator()
        generator.packets = packets
        
        # Setup modifications
        for pkt in packets:
            isIPModified = False
            isPortModified = False
            isMacModified = False
            if pkt.haslayer(IP) and not isIPModified:
                if args.src is not None:
                    generator.setupIPAddr(pkt[IP].src, args.src)
                    isIPModified = True
                if args.dst is not None:
                    generator.setupIPAddr(pkt[IP].dst, args.dst)
                    isIPModified = True
                if args.src is None and args.dst is None:
                    isIPModified = True
            
            if pkt.haslayer(TCP) and not isPortModified:
                if args.sport is not None:
                    generator.setupPort(pkt[TCP].sport, args.sport)
                    isPortModified = True
                if args.dport is not None:
                    generator.setupPort(pkt[TCP].dport, args.dport)
                    isPortModified = True
                if args.sport is None and args.dport is None:
                    isPortModified = True

            if pkt.haslayer(Ether) and not isMacModified:
                if args.smac is not None:
                    generator.setupMac(pkt[Ether].src, args.smac)
                    isMacModified = True
                if args.dmac is not None:
                    generator.setupMac(pkt[Ether].dst, args.dmac)
                    isMacModified = True
                if args.smac is None and args.dmac is None:
                    isMacModified = True
            
            if isIPModified and isPortModified and isMacModified:
                break
        
        # Setup connectivity
        generator.setupInterface(args.interface)

        # Generate Traffic!
        generator.sendPackets()
    