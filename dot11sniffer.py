#!/bin/python2

import time

from sniffer_module import *
from threading import *

import signal
import sys
import netifaces

# globals
shouldQuit = None
otherThread = None

# signal handler
def sigintHandler(signum, frame):
    print("Quitting uncleanly")
    sys.exit()

# search for interfaces until we found a monitor interface
def findIface():
    chosenIface = None
    while chosenIface is None:
        ifaces = netifaces.interfaces()
        for iface in ifaces:
            if iface[:3] == 'mon':
                chosenIface = iface

    return chosenIface

# gets hostname for computer
def getHostname():
    hostnameFile = open("/etc/hostname", "r")
    hostname = hostnameFile.readline()
    hostnameFile.close()

    return hostname

def main():
    # register signal handler and then sleep until we get a response
    signal.signal(signal.SIGINT, sigintHandler)

    # init the processing thread
    shouldQuit = False
    listLock = Lock()
    otherThread = ProcessingThread(listLock, shouldQuit)

    # find monitor inferaces
    print("Looking for monitor interfaces...")
    chosenIface = findIface()
    print("Found Interface: " + chosenIface)

    # get the hostname
    hostname = getHostname()
    print("Hostname: " + hostname)

    # start the other thread to start sniffing
    otherThread.start()

    # sit and spin while the other thread does things
    while True:
        time.sleep(1)

# run main
if __name__ == "__main__":
    main()
