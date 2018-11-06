def get_sign(n):
    """
    Gets the sign of a given number
    :param n: Number
    :return: returns 1 with the sign given (ex. -300 would return -1)
    """
    if n < 0:
        return -1
    else:
        return 1

def adjusted_fs(fs, fy):
    """
    Adjust the fs based on fy.
    :param fs: actual stress based on strain diagram
    :param fy: yield stress of steel
    :return: fs
    """
    if abs(fs) >= fy:
        return fy * get_sign(fs)
    else:
        return fs

def get_fs(dist, c, fy):
    """
    Get the fs based on strain diagram
    :param dist: distance of steel from extreme compression fiber
    :param c: depth of neutral axis
    :param fy: yield stress of steel
    :return: fs
    """
    if dist <= c:
        fs = 600 * (c - dist) / c
    else:
        fs = -600 * (dist + c) / c
    return adjusted_fs(fs, fy)
