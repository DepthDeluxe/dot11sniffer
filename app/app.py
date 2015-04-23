import time
import math
import DBFinder
import Trilateration_Colin

# sniffers are
# [ sniffer-0, sniffer-1, sniffer-something ]
snifferPositions = [Trilateration_Colin.Point(361, 231), Trilateration_Colin.Point(338, 617), Trilateration_Colin.Point(194, 665)]

def main():
    # set the sniffer positions appropriate location in BRKI1
    finder = DBFinder.DBFinder()

    # get a list of all timeblocks
    ids = finder.findIds()

    # process the trilateration for each timeblock
    for ident in ids:
        print(ident)
        processTrilateration(ident, finder)

    # pull points for the most recent block
    points = finder.pull_processed_block(math.floor(time.time() / 600) - 3)
    uniq = finder.pull_processed_uniq(math.floor(time.time() / 600) - 3)
    print(points)
    print(uniq)

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
