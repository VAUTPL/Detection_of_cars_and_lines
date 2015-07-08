__author__ = 'utpl'


def isBelow((rX, rY, rW, rH), (pt1x, pt1y), (pt2x, pt2y)):
    v1 = [pt2x-pt1x, pt2y-pt1y]   # Vector 1
    v2 = [pt2x-rY, pt2y-(rX+rW)]   # Vector 2
    xp = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product
    return xp > 0