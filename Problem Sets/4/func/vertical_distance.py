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