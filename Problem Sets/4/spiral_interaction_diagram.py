from func.utilities import *
from func.integral import *
from func.stresses import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.axes as axes

# = = = = = = = = = = = = = = = = = = = = = = #
#              Input parameters               #
# = = = = = = = = = = = = = = = = = = = = = = #

# Height of circular section, set to unity
h = 1.0

# Factor to determine distance between top and bottom bars
gamma = 0.8

# Number of bars, minimum of 8 bars
bar_qty = 12

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
balanced_condition_x = [0.0]
balanced_condition_y = [0.0]
# --> Zero strain at tension bar
et_zero_x = [0.0]
et_zero_y = [0.0]
# --> Tension at 0.5Fy
half_fy_x = [0.0]
half_fy_y = [0.0]
# --> Maximum strain permitted
max_strain_x = [0.0]
max_strain_y = [0.0]

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

    # At maximum strain permitted by code
    c = 0.003 * farthest / 0.008
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

    max_strain_x.append(sum_of_moment * phi / gross_area / h / fc_prime)
    max_strain_y.append(sum_of_forces * phi / gross_area / fc_prime)

# = = = = = = = = = = = = = = = = = = = = = = #
#                   Plotting                  #
# = = = = = = = = = = = = = = = = = = = = = = #
plt.figure(figsize=(5, 8))
plt.title("DIMENSIONLESS INTERACTION DIAGRAM\n(SPIRAL COLUMN)")
plt.xlabel(r"$\dfrac{\phi \cdot M_n}{f'c \cdot A_g \cdot h}$")
plt.ylabel(r"$\dfrac{\phi \cdot P_n}{f'c \cdot A_g}$")

# Grid setting
h_spacing = 0.01
v_spacing = 0.1
minorlocator_x = MultipleLocator(h_spacing)
minorlocator_y = MultipleLocator(v_spacing)
plt.gca().xaxis.set_minor_locator(minorlocator_x)
plt.gca().yaxis.set_minor_locator(minorlocator_y)
plt.grid(which='minor')

# Texts
text_balanced_condition = r"$f_s = f_y$"
text_zero_strain = r"$\epsilon_t = 0$"
text_half_fy = r"$f_s = \dfrac{1}{2} \cdot f_y$"
text_max_strain = r"$\epsilon_t = 0.005$"

# Text plots
plt.text(balanced_condition_x[len(balanced_condition_x) - 1],
         balanced_condition_y[len(balanced_condition_y) - 1],
         text_balanced_condition, fontsize=14)
plt.text(et_zero_x[len(et_zero_x) - 1],
         et_zero_y[len(et_zero_y) - 1],
         text_zero_strain, fontsize=14)
plt.text(half_fy_x[len(half_fy_x) - 1],
         half_fy_y[len(half_fy_y) - 1],
         text_half_fy, fontsize=14)
plt.text(max_strain_x[len(max_strain_x) - 1],
         max_strain_y[len(max_strain_y) - 1],
         text_max_strain, fontsize=14)

farthest_moment = farthest_distance(x_components[len(x_components) - 1])
highest_axial = farthest_distance(y_components[len(y_components) - 1])
legend_location_x = farthest_moment
legend_location_y = highest_axial

# Change the axis limit in x-direction
# axes.Axes.set_xlim(right=farthest_moment * 2)
plt.xlim(right=farthest_moment * 3 / 2)

# Curves
plt.plot(balanced_condition_x, balanced_condition_y, ':')
plt.plot(et_zero_x, et_zero_y, ':')
plt.plot(half_fy_x, half_fy_y, ':')
plt.plot(max_strain_x, max_strain_y, ':')

# Plot of curves
for i in range(len(x_components)):
    i, = plt.plot(x_components[i], y_components[i])

# Texts for rho
for j in range(len(rho_collection)):
    text_rho = r"$\rho=$" + str(round(rho_collection[j] * 100, 0)) + "%"
    text_coord_x = x_components[j][2]
    text_coord_y = y_components[j][2]
    plt.text(text_coord_x, text_coord_y, text_rho, backgroundcolor=(1, 1, 1), fontsize=9)

plt.show()
