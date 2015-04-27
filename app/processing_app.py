import time
import math
import DBFinder
import dbCompressor
import os
import Trilateration_Colin
import matplotlib

# sniffers are
# [ sniffer-0, sniffer-1, sniffer-something ]
snifferPositions = [Trilateration_Colin.Point(361, 231), Trilateration_Colin.Point(338, 617), Trilateration_Colin.Point(194, 665)]

def dist( x1, x2, y1, y2 ):
    d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
    if d==0.0:
        return 1.0
    else:
        return d

def plotLocations():
    f = DBFinder()
    l = f.findIds()

    d = f.pull_processed_block(l[-2])

    sizeX = 904
    sizeY = 1033
    numBins = 2.0
    xi = np.arange(0.0, float(sizeX))
    yi = np.arange(0.0, float(sizeY))
    locationsX = []
    locationsY = []
    for i in range(0, len(d)):
	locationsX += [d[i][0]]
	locationsY += [d[i][1]]

    scale = 0.5
    dpi = 80
    # 80 dots/inch * 12 inches/foot * 5 feet/32 pixels = 150
    lena = Image.open('/var/www/html/images/brki_w_nodes.png')
    figsize = scale*lena.size[0]/dpi, scale*lena.size[1]/dpi
    fig = plt.figure(figsize=figsize)

    ax = fig.add_subplot(111)
    ax.imshow(lena)

    ax.plot(locationsX, locationsY,'o')
    ax.set_xlim(0, len(xi))
    ax.set_ylim(0, len(yi))
    ax.set_title("Muenster Cheese")
    fig.savefig("test.png", pad_inches=0)
    plt.close(fig)

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
