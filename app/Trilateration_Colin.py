import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def rssToEstimatedDistance(rss):
    freq = 2462             # freq of WiFi channel 6
    origDBm = -20           # estimate this value
    loss = abs(origDBm - rss)
    dist = 10 ** ( ( loss + 27.55 - 20 * math.log10(freq) ) / 20 )

    return dist

def trilaterate(inSources, rss):
    distances = []
    distances.append( rssToEstimatedDistance(rss[0]) )
    distances.append( rssToEstimatedDistance(rss[1]) )
    distances.append( rssToEstimatedDistance(rss[2]) )

    # find the three intersection points
    tp1 = _findEqualPerp(inSources[0], inSources[1], distances[0], distances[1])
    tp2 = _findEqualPerp(inSources[0], inSources[2], distances[0], distances[2])
    tp3 = _findEqualPerp(inSources[1], inSources[2], distances[1], distances[2])

    p = Point( (tp1.x + tp2.x + tp3.x) / 3, (tp1.y + tp2.y + tp3.y) / 3 )
    return p

def _findEqualPerp(p1, p2, r1, r2):
    # swap points if p2 is behind p2
    if p2.x < p1.x:
        temp = p2
        p2 = p1
        p1 = temp

    # compute the equation for the line
    deltaX = p2.x - p1.x
    deltaY = p2.y - p1.y
    if deltaX == 0:
        slope = 999999999
    else:
        slope = deltaY / deltaX
    intercept = p2.y - slope * p2.x

    # compute the constant multiplier
    lineLen = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    c = lineLen / (r1 + r2)

    posOnLine = c * r1
    angle = math.atan(slope)

    touchingPoint = Point(math.cos(angle) * posOnLine + p1.x, math.sin(angle) * posOnLine + p1.y)

    return touchingPoint

# test program
def main():
    a = Point(1, 6)
    b = Point(2, 3)
    c = Point(5, 7)

    t = trilaterate([a,b,c], [2,3,5])
    print(t.x)
    print(t.y)

if __name__ == '__main__':
    main()
