import math
from func.utilities import *
from func.integral import *

# = = = = = = = = = = = = = = = = = = = = = = #
#              Input parameters               #
# = = = = = = = = = = = = = = = = = = = = = = #

# Height of circular section, set to unity
h = 1.0

# Factor to determine distance between top and bottom bars
gamma = 0.8

# Number of bars, minimum of 8 bars
bar_qty = 9

# Steel to concrete ratio to be created with interaction diagram
rho_collection = [.01]  #, .02, .03, .04, .05, .06, .07, .08]

# Materials parameters
fy = 415
fc_prime = 21

# = = = = = = = = = = = = = = = = = = = = = = #
#           Calculated parameters             #
# = = = = = = = = = = = = = = = = = = = = = = #

# Gross area of circle
gross_area = math.pi / 4 * (h ** 1)

# Distance between reinforcement and the concrete edge.
# Assuming the are exactly one bar at top and one bar at bottom.
d1 = (h - gamma * h) / 2

# Distance between the top concrete fiber and the bottom reinforcement
d = h - d1

# Radius up to location of bars
bar_radius = gamma * h / 2

# Angle between two bars
angle_between_bars = 360 / bar_qty

# Beta 1
beta_1 = 0.85 - 0.05 / 7 * (fc_prime - 28) if fc_prime > 28 else 0.85

# Bar distance from the top
bar_distances = []

for i in range(bar_qty):
    dist = d1 + vertical_distance(gamma * h / 2, angle_between_bars * i)
    bar_distances.append(dist)

# = = = = = = = = = = = = = = = = = = = = = = #
#              Iterative process              #
# = = = = = = = = = = = = = = = = = = = = = = #
for i in range(len(rho_collection)):
    bars_area = rho_collection[i] * gross_area
    bar_area = bars_area / bar_qty
    print("= = = = rho : " + str(rho_collection[i]) + " = = = = = = =")

    rebars = []
    for i in range(bar_qty):
        rebars.append((bar_area, bar_distances[i], fy))
    concrete = (gross_area, 0.5, fc_prime)

    pna = pna_from_top(concrete, rebars)
    print(round(pna, 2))
    c = 0.0001
    a = beta_1 * c
    x = 0.0001

    while x > 0.0:
        x -= 0.0001

        for j in range(bar_qty):
            print("As # = " + str(j + 1) +
                  " | Dist. from Top = " + str(round(bar_distances[j], 4)))

