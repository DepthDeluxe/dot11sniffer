import time
import math
import DBFinder
import dbCompressor
import os
import Trilateration_Colin
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import imageMaker

# sniffers are
# [ sniffer-0, sniffer-1, sniffer-something ]
snifferPositions = [Trilateration_Colin.Point(391, 61), Trilateration_Colin.Point(220, 715), Trilateration_Colin.Point(1233, 717)]

def plotLocations():
    finder = DBFinder.DBFinder()
    times = finder.findIds()

    pos = finder.pull_processed_block(times[-2])
    
    im = imageMaker.ImageMaker('larrison-floorplan.png')
    for point in pos:
        im.addPoint(point[0],point[1])
    im.saveImage()
    

def writePIDFile():
    f = open("./processing.pid", "w")
    f.write(str(os.getpid()))
    f.close()

def main():
    # write the PID file so we know where its running
    writePIDFile()

    oldBlock = 0
    while True:
        # process only if we moved timeblocks
        curBlock = math.floor( time.time() / 600 )
        if curBlock != oldBlock:
            oldBlock = curBlock
            print("processing: " + str(curBlock))
            process()
            plotLocations()

        # sleep for another 5 seconds
        time.sleep(5)

def process():
    # set the sniffer positions appropriate location in BRKI1
    finder = DBFinder.DBFinder()
    compressor = dbCompressor.Compress()

    # get a list of all timeblocks
    ids = finder.findIds()

    # get a list of processed timeblocks
    processedIds = finder.findProcessedIds()

    # get a list of ids to process
    idsToProcess = [ x for x in ids if x not in processedIds ]

    # process the trilateration for each timeblock
    for ident in idsToProcess:
        print(ident)
        processTrilateration(ident, finder)

        # pull the data for compression
        data = finder.pull(ident)
        compressor.upload(ident, data)


def processTrilateration(timeblock, finder):
    # use the previous timeblock
    macs = {}
    inData = finder.pull(timeblock)
    for entry in inData:
        mac = entry['mac']
        if mac not in macs:
            macs[mac] = {}
        macs[mac][entry['node']] = [ entry['sigstr'], entry['time'] ]

    numMacs = len(macs)

    triples = []
    for mac in reversed(list(macs.keys())):
        if ( len(macs[mac]) == 3 ):
            triples.append(macs[mac])

    points = []
    for triple in triples:
        val = Trilateration_Colin.trilaterate(snifferPositions, [ triple['sniffer-0'][0], triple['sniffer-1'][0], triple['sniffer-something'][0] ])

        points.append((val.x, val.y))

    finder.write_processed_block(timeblock, points, numMacs)

if __name__ == "__main__":
    main()
