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
# register signal handler and then sleep until we get a response
signal.signal(signal.SIGINT, sigintHandler)

# init the processing thread
shouldQuit = False
listLock = Lock()
otherThread = ProcessingThread(listLock, shouldQuit)

# search for interfaces until we found a monitor interface
print("Looking for monitor interfaces...")
chosenIface = None
while chosenIface is not None:
    ifaces = netifaces.interfaces()
    for iface in ifaces:
        if iface[:3] == 'mon':
            chosenIface = iface


# start the other thread to start sniffing
otherThread.start()

# sit and spin while the other thread does things
while True:
    time.sleep(1)
