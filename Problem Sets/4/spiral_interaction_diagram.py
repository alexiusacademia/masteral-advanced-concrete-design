import math
from func.vertical_distance import *

# = = = = = = = = = = = = = = = = = = = = = = #
#              Input parameters               #
# = = = = = = = = = = = = = = = = = = = = = = #

# Height of circular section, set to unity
h = 1.0

# Factor to determine distance between top and bottom bars
gamma = 0.8

# Number of bars, minimum of 8 bars
bar_qty = 8

# Steel to concrete ratio to be created with interaction diagram
rho_collection = [.01]  #, .02, .03, .04, .05, .06, .07, .08]

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

# Bar distance from the top
bar_distances = []
for i in range(bar_qty):
    dist = d1 + vertical_distance(gamma * h / 2, angle_between_bars * i)
    bar_distances.append(dist)

for i in range(len(rho_collection)):
    bars_area = rho_collection[i] * gross_area
    bar_area = bars_area / bar_qty
    print("= = = = rho : " + str(rho_collection[i]) + " = = = = = = =")
    for j in range(bar_qty):
        print("As # = " + str(j + 1) +
              " | Dist. from Top = " + str(round(bar_distances[j], 4)))
