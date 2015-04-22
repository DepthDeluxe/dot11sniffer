import math


_snifferPositions = [[0, 0], [8, 0], [4, 8]]
areaWidth = 8
areaHeight = 8

def setSnifferPositions(positions):
    global _snifferPositions
    _snifferPositions = positions

def getDistanceToSniffer(signalStrength, pathLossExponent):
	"""Calculates the estimated distance using the signal strength.
		 The model used to calculate the distance can be found here: http://www.ee.ucl.ac.uk/lcs/previous/LCS2005/12.pdf"""
	tmp = (signalStrength + 40.0459970203) * (2.30258509299/ ((-10.0) * pathLossExponent))
	return math.exp(tmp)


def getDeviceLocation(signalStrength1, signalStrength2, signalStrength3):
	"""Calculates the estimated distance to each sniffer and return the position (x, y) of the device."""
	snifferDistance1 = getDistanceToSniffer(signalStrength1, 4)
	snifferDistance2 = getDistanceToSniffer(signalStrength2, 4)
	snifferDistance3 = getDistanceToSniffer(signalStrength3, 4)

	errorMatrix = [[0 for x in range(areaWidth)] for y in range(areaHeight)]
	minY = 0
	minX = 0
	for y in range(areaHeight):
		for x in range(areaWidth):
			errorMatrix[y][x] += math.pow(math.sqrt(math.pow((x + 0.5) - _snifferPositions[0][0], 2.0) + math.pow((y + 0.5) - _snifferPositions[0][1], 2.0)) - snifferDistance1, 2.0)
			errorMatrix[y][x] += math.pow(math.sqrt(math.pow((x + 0.5) - _snifferPositions[1][0], 2.0) + math.pow((y + 0.5) - _snifferPositions[1][1], 2.0)) - snifferDistance2, 2.0)
			errorMatrix[y][x] += math.pow(math.sqrt(math.pow((x + 0.5) - _snifferPositions[2][0], 2.0) + math.pow((y + 0.5) - _snifferPositions[2][1], 2.0)) - snifferDistance3, 2.0)
			if(errorMatrix[y][x] < errorMatrix[minY][minX]):
				minY = y
				minX = x

	return minX, minY


if __name__ == "__main__":
    print(getDeviceLocation(-75, -60, -60))
