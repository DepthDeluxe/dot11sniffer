import time

from sniffer_module import *
from threading import *

import signal
import sys

# globals
shouldQuit = None
otherThread = None

def sigintHandler(signum, frame):
    print("Quitting uncleanly")
    sys.exit()

# init the processing thread
shouldQuit = False
listLock = Lock()
otherThread = ProcessingThread(listLock, shouldQuit)

# start the other thread to start sniffing
otherThread.start()

# register signal handler and then sleep until we get a response
signal.signal(signal.SIGINT, sigintHandler)

# sit and spin while the other thread does things
while True:
    time.sleep(1)
