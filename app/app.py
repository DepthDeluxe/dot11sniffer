import time
import math
import DBFinder
import Trilateration

macs = []

def main():
    # set the sniffer positions appropriate location in BRKI1
    Trilateration.setSnifferPositions([[367,236], [336,610], [191,633]])
    finder = DBFinder.DBFinder()

    # use the previous timeblock
    timeblock = math.floor(time.time() / 600) - 1
    data = finder.pull(timeblock)
    for entry in data:
        if entry['mac'] not in macs:
            macs.append(entry['mac'])
    finder.set_num_unique(timeblock, len(macs))

if __name__ == "__main__":
    main()
