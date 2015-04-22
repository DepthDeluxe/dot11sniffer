import time
import math
import DBFinder
import Trilateration_Colin

macs = {}
snifferPositions = [Trilateration_Colin.Point(361, 231), Trilateration_Colin.Point(338, 617), Trilateration_Colin.Point(194, 665)]

# sniffers are
# sniffer-0, sniffer-1, sniffer-something
def main():
    # set the sniffer positions appropriate location in BRKI1
    finder = DBFinder.DBFinder()

    # use the previous timeblock
    timeblock = math.floor(time.time() / 600) - 1
    data = finder.pull(timeblock)
    for entry in data:
        mac = entry['mac']
        if mac not in macs:
            macs[mac] = {}
        macs[mac][entry['node']] = [ entry['sigstr'], entry['time'] ]

    print(macs)

    triples = []
    for mac in reversed(list(macs.keys())):
        if ( len(macs[mac]) == 3 ):
            triples.append(macs[mac])

    for triple in triples:
        val = Trilateration_Colin.trilaterate(snifferPositions, [ triple['sniffer-0'][0], triple['sniffer-1'][0], triple['sniffer-something'][0] ])

        print((val.x, val.y))

if __name__ == "__main__":
    main()
