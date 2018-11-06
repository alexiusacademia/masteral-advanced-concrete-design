from func.utilities import *
from func.integral import *
from func.stresses import *
import matplotlib.pyplot as plt

# = = = = = = = = = = = = = = = = = = = = = = #
#              Input parameters               #
# = = = = = = = = = = = = = = = = = = = = = = #

# Height of circular section, set to unity
h = 1.0

# Factor to determine distance between top and bottom bars
gamma = 0.8

# Number of bars, minimum of 8 bars
bar_qty = 10

# Steel to concrete ratio to be created with interaction diagram
rho_collection = [.01, .02, .03, .04, .05, .06, .07, .08]

# Materials parameters
fy = 275
fc_prime = 21

# = = = = = = = = = = = = = = = = = = = = = = #
#           Calculated parameters             #
# = = = = = = = = = = = = = = = = = = = = = = #

# Radius of circle
radius = h / 2.0

# Gross area of circle
gross_area = math.pi / 4 * (h ** 2)

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

# Bar distances from the top
bar_distances = []

for i in range(bar_qty):
    dist = d1 + vertical_distance(gamma * h / 2, angle_between_bars * i)
    bar_distances.append(dist)

# Variables to hold values to be plotted
x_components = []
y_components = []

# Major points
# --> Balanced condition
balanced_condition_x = []
balanced_condition_y = []
# --> Zero strain at tension bar
et_zero_x = []
et_zero_y = []
# --> Tension at 0.5Fy
half_fy_x = []
half_fy_y = []

# = = = = = = = = = = = = = = = = = = = = = = #
#              Iterative process              #
# = = = = = = = = = = = = = = = = = = = = = = #
for i in range(len(rho_collection)):
    # x and y component for each rho value
    xs = []
    ys = []

    # Total area of reinforcements in terms of h
    bars_area = rho_collection[i] * gross_area

    # Area of a single bar
    bar_area = bars_area / bar_qty

    print("= = = = rho : " + str(rho_collection[i]) + " = = = = = = =")

    # Calculation of plastic neutral axis
    # -> List of rebars object (rebar area, distance from top, yield strength)
    rebars = []
    for i in range(bar_qty):
        rebars.append((bar_area, bar_distances[i]))

    # -> Concrete object (area, centroid measured from top, compressive strength)
    concrete = (gross_area, 0.5)

    # Plastic neutral axis location from top
    pna = pna_from_top(concrete, rebars, fc_prime, fy)

    # Calculation of:
    #           phi . Pn                 phi . Mn
    #  [y] --> ----------  and  [x] --> ----------
    #              Ag                      Ag.h

    # Initial values for iteration process
    c = 0.0001
    a = beta_1 * c
    y_cc = pna - compression_centroid_from_top(radius, radius - a)
    cc = 0.85 * fc_prime * compression_area(radius, radius - a)
    m_conc = cc * y_cc

    # Get the farthest distance and calculate strain
    farthest = farthest_distance(bar_distances)
    ety = fy / 200000
    et = (farthest - c) * 0.003 / c
    et_prev = et
    phi = 0.75
    if et < ety:
        phi = 0.75
    elif (et > ety) and (et < 0.005):
        phi = 0.75 + 0.15 * (et - ety) / (0.005 - ety)
    else:
        phi = 0.9

    # Summation of forces initialized to concrete compression
    sum_of_forces = cc

    # Summarion of moments initialized to concrete bending
    sum_of_moment = m_conc

    # Iterate through each bar
    for j in range(bar_qty):
        fs = get_fs(bar_distances[j], c, fy)
        fs_corrected = fs if get_sign(fs) < 0 else fs - 0.85 * fc_prime
        y_rebar = pna - bar_distances[j]
        f_steel = fs_corrected * bar_area
        m_steel = f_steel * y_rebar
        sum_of_forces += f_steel
        sum_of_moment += m_steel

    xs.append(sum_of_moment * phi / gross_area / h / fc_prime)
    ys.append(sum_of_forces * phi / gross_area / fc_prime)

    # Interval for iteration on c
    c_interval = 0.05

    while sum_of_moment > 0.0:
        c += c_interval

        # phi calculation
        et = (farthest - c) * 0.003 / c
        phi = 0.75
        if et < ety:
            phi = 0.75
        elif (et > ety) and (et < 0.005):
            phi = 0.75 + 0.15 * (et - ety) / (0.005 - ety)
        else:
            phi = 0.9

        a = beta_1 * c

        y_cc = pna - compression_centroid_from_top(radius, radius - a)
        cc = 0.85 * fc_prime * compression_area(radius, radius - a)
        m_conc = cc * y_cc

        sum_of_forces = cc
        sum_of_moment = m_conc

        for j in range(bar_qty):
            fs = get_fs(bar_distances[j], c, fy)
            fs_corrected = fs if (get_sign(fs) < 0) else (fs - 0.85 * fc_prime)
            y_rebar = pna - bar_distances[j]
            f_steel = fs_corrected * bar_area
            m_steel = f_steel * y_rebar
            sum_of_forces += f_steel
            sum_of_moment += m_steel

        xs.append(sum_of_moment * phi / gross_area / h / fc_prime)
        ys.append(sum_of_forces * phi / gross_area / fc_prime)

        # print("phi.Mn/(f'c.Ag.h) = " + str(round(sum_of_moment * phi / gross_area / h / fc_prime, 4)) +
        #      ", phi.Pn/(f'c.Ag) = " + str(round(sum_of_forces * phi / gross_area / fc_prime, 4)) +
        #      ", Cc arm = " + str(round(y_cc, 10)), ", phi = " + str(round(phi, 4)))

    x_components.append(xs)
    y_components.append(ys)

    # Balanced condition
    cb = 600 * farthest / (fy + 600)
    et = (farthest - c) * 0.003 / c
    phi = 0.75
    if et < ety:
        phi = 0.75
    elif (et > ety) and (et < 0.005):
        phi = 0.75 + 0.15 * (et - ety) / (0.005 - ety)
    else:
        phi = 0.9
    ab = cb * beta_1
    y_cc = pna - compression_centroid_from_top(radius, radius - ab)
    cc = 0.85 * fc_prime * compression_area(radius, radius - ab)
    m_conc = cc * y_cc

    sum_of_forces = cc
    sum_of_moment = m_conc

    for j in range(bar_qty):
        fs = get_fs(bar_distances[j], cb, fy)
        fs_corrected = fs if (get_sign(fs) < 0) else (fs - 0.85 * fc_prime)
        y_rebar = pna - bar_distances[j]
        f_steel = fs_corrected * bar_area
        m_steel = f_steel * y_rebar
        sum_of_forces += f_steel
        sum_of_moment += m_steel

    balanced_condition_x.append(sum_of_moment * phi / gross_area / h / fc_prime)
    balanced_condition_y.append(sum_of_forces * phi / gross_area / fc_prime)

    # Zero strain at tension
    c = farthest
    et = (farthest - c) * 0.003 / c
    phi = 0.75
    if et < ety:
        phi = 0.75
    elif (et > ety) and (et < 0.005):
        phi = 0.75 + 0.15 * (et - ety) / (0.005 - ety)
    else:
        phi = 0.9

    a = beta_1 * c

    y_cc = pna - compression_centroid_from_top(radius, radius - a)
    cc = 0.85 * fc_prime * compression_area(radius, radius - a)
    m_conc = cc * y_cc

    sum_of_forces = cc
    sum_of_moment = m_conc

    for j in range(bar_qty):
        fs = get_fs(bar_distances[j], c, fy)
        fs_corrected = fs if (get_sign(fs) < 0) else (fs - 0.85 * fc_prime)
        y_rebar = pna - bar_distances[j]
        f_steel = fs_corrected * bar_area
        m_steel = f_steel * y_rebar
        sum_of_forces += f_steel
        sum_of_moment += m_steel

    et_zero_x.append(sum_of_moment * phi / gross_area / h / fc_prime)
    et_zero_y.append(sum_of_forces * phi / gross_area / fc_prime)

    # At 0.5Fy
    c = 600 * farthest / (0.5 * fy + 600)
    et = (farthest - c) * 0.003 / c
    phi = 0.75
    if et < ety:
        phi = 0.75
    elif (et > ety) and (et < 0.005):
        phi = 0.75 + 0.15 * (et - ety) / (0.005 - ety)
    else:
        phi = 0.9

    a = beta_1 * c

    y_cc = pna - compression_centroid_from_top(radius, radius - a)
    cc = 0.85 * fc_prime * compression_area(radius, radius - a)
    m_conc = cc * y_cc

    sum_of_forces = cc
    sum_of_moment = m_conc

    for j in range(bar_qty):
        fs = get_fs(bar_distances[j], c, fy)
        fs_corrected = fs if (get_sign(fs) < 0) else (fs - 0.85 * fc_prime)
        y_rebar = pna - bar_distances[j]
        f_steel = fs_corrected * bar_area
        m_steel = f_steel * y_rebar
        sum_of_forces += f_steel
        sum_of_moment += m_steel

    half_fy_x.append(sum_of_moment * phi / gross_area / h / fc_prime)
    half_fy_y.append(sum_of_forces * phi / gross_area / fc_prime)

# = = = = = = = = = = = = = = = = = = = = = = #
#                   Plotting                  #
# = = = = = = = = = = = = = = = = = = = = = = #
plt.figure(figsize=(10, 8))
plt.title("Dimensionless Interaction Diagram of Spiral Column")
plt.xlabel(r"$\dfrac{\phi \cdot M_n}{f'c \cdot A_g \cdot h}$")
plt.ylabel(r"$\dfrac{\phi \cdot P_n}{f'c \cdot A_g}$")
plt.grid()

plt.plot(balanced_condition_x, balanced_condition_y, ':')
plt.plot(et_zero_x, et_zero_y, ':')
plt.plot(half_fy_x, half_fy_y, ':')

for i in range(len(x_components)):
    i, = plt.plot(x_components[i], y_components[i])

plt.show()
