import math

iteration = 10000.0


def compression_area(r, y1):
    """
    Calculates the area of a circular segment
    :param r: radius of the circle
    :param y1: radius minus height of the secment
    :return: area
    """
    area = 0.0
    dy = (r - y1) / iteration

    for i in range(int(iteration)):
        y = r - (i * dy)
        if abs(y) > r:
            break
        strip = math.sqrt(r**2 - y**2) * dy * 2
        area += strip

    return area


def compression_centroid_from_top(r, y1):
    """
    Calculates the centroid of a compression area of a
    circular segment from the top
    :param r: radius formed by centroids of rebars
    :param y1: radius minus height of the segment
    :return: y-bar from top
    """
    area = compression_area(r, y1)
    dy = (r - y1) / iteration
    moment_area = 0.0

    for i in range(int(iteration)):
        y = r - (i * dy)
        if abs(y) > r:
            break
        m_a = math.sqrt(r**2 - y**2) * y * dy * 2
        moment_area += m_a

    return r - moment_area / area

