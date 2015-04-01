from scapy.all import *

import threading
import time

class ProcessingThread(threading.Thread):
    def __init__(self, listLock, shouldQuit):
        # initialize super
        super(ProcessingThread, self).__init__()

        # turn on daemonize so we close when we should
        self.daemon = True

        # store copies of the array
        self.listLock = listLock
        self.shouldQuit = shouldQuit

        # init other variables
        self.accessPoints = {}
        self.devices = {}

        self.numProcessed = 0

    def run(self):
        # start sniffing
        sniff(iface="mon0", prn=self._sniffDot11Beacon)

    def _printNumActiveDevices(self):
        # counts the number of devices that have been around in
        # the past 5 minutes
        currentEpochTime = int(time.time())
        numActive = 0
        for ssid in self.devices:
            diff = currentEpochTime - self.devices[ssid]
            if ( diff < 300 ):
                numActive += 1

        print("# Devices: " + str(numActive))

    def _addMACtoAPList(self, ssid, mac):
        # check to see if we have already added the access point
        # if we have, then check to see if the current MAC is in
        # the list of MAC addresses associated with that ap
        if ssid in self.accessPoints:
            macList = self.accessPoints[ssid]
            if mac in macList:
                return
            else:
                macList.append(mac)
        else:
            self.accessPoints[ssid] = [mac]

    def _addMACToList(self, mac):
        # lock access to the devices list
        self.listLock.acquire()

        # get the current time
        currentEpochTime = int(time.time())

        # add the MAC address to the list of devices if it already
        # isn't in there, otherwise update time we last saw it
        self.devices[mac] = currentEpochTime

        # unlock access to the devices list
        self.listLock.release()

    def _cleanDevicesList(self):
        # acquire a lock on the devices list
        self.listLock.acquire()

        # search for MACs in devices that are in APs
        for mac in self.devices:
            for ssid in self.accessPoints:
                for ssidMAC in self.accessPoints[ssid]:
                    # if the MACs match, then remove the device from the
                    # devices list
                    if mac == ssidMAC:
                        self.devices.pop(mac, None)

        # release the lock
        self.listLock.release()

    # sniff all 802.11 beacons and store in a list
    def _sniffDot11Beacon(self, pkt):
        # increment the processing counter
        self.numProcessed += 1

        if pkt.haslayer(Dot11Beacon):
            # get the 802.11 layer and the information element layer
            dot11Layer = pkt.getlayer(Dot11)
            beaconElt = pkt.getlayer(Dot11Elt)[0]

            # get the MAC address and ssid
            macAddr = dot11Layer.addr2
            ssid = beaconElt.info

            # put into list
            self._addMACtoAPList(ssid, macAddr)
        elif pkt.haslayer(Dot11):
            # get the 802.11 layer and pull the MAC address
            dot11Layer = pkt.getlayer(Dot11)

            self._addMACToList(dot11Layer.addr2)
            self._printNumActiveDevices()

        # clean devices list every 25000 packets
        if self.numProcessed % 25000 == 0:
            self._cleanDevicesList()
