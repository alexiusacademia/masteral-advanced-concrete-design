import math

def vertical_distance(r, theta):
    y = 0
    x = 0
    if theta < 180:
        x = 2 * r * math.sin(theta / 2 * math.pi / 180)
        alpha = (180 - theta) / 2
    else:
        beta = 360 - theta
        x = 2 * r * math.sin(beta / 2 * math.pi / 180)
        alpha = (180 - beta) / 2
    y = x * math.cos(alpha * math.pi / 180)

    return y

def pna_from_top(concrete, rebars, fc_prime, fy):
    """
    Calculates the distance from plastic neutral axis to the top
    of concrete using varignon's theorem
    :param concrete: a tuple (area, centroid from top, f'c)
    :param rebars:  a list of tuple for steel bars (area, centroid from top, fy)
    :return: pna from top
    """
    total_force = concrete[0] * fc_prime
    total_moment = concrete[0] * fc_prime * concrete[1]
    for rebar in rebars:
        total_force += rebar[0] * fy
        total_moment += rebar[0] * fy * rebar[1]

    return total_moment / total_force

def farthest_distance(distances):
    farthest = 0
    for dist in distances:
        if dist > farthest:
            farthest = dist

    return farthest