# ----------------------------------------------
# Imports
# ----------------------------------------------
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import OffsetFrom

# ----------------------------------------------
# Problem definition
# ----------------------------------------------
fcPrime = 27.5
fy = 275
b = 375                     # Web
d = 570                     # Effective depth
DL = 45                     # kN/m
LL = 60                     # kN/m
L = 6000                    # mm
a = L / 2                   # Half of beam
As = 3000                   # 4 - 20mm dia.
p = As / (b * d)            # rho, steel-concrete ratio
no_of_increment = 1000

# ----------------------------------------------
# Constants / Factors
# ----------------------------------------------
dl_factor = 1.2             # Deadload factor
ll_factor = 1.6             # Liveload factor

# ----------------------------------------------
# Calculations
# ----------------------------------------------
# 1. Vc using simplified method
vc_simplified = 1 / 6 * math.sqrt(fcPrime) * b * d

# 2. Vc using more detailed formula
# 2.1. Total Factored load
wu = dl_factor * DL + ll_factor * LL

# 2.2. Calculate reaction at left support (A)
r_a = wu * L / 2

# 2.3. For the shear envelop
r_be = ll_factor * LL * a * (a / 2) / L

# 2.4. Analyze half of the beam
# Discretize half of beam by 1000 division
increment = a / no_of_increment

# 2.4.1. Variables for calculated values
xs = []                     # Values of x at discrete points
simp = []                   # Values of Vc (simplified) at every point
vcs = []                    # Values of Vc (detailed) at every point
vus = []                    # Values of Vu at every point (envelope)
beam = []                   # Ordinate of beam element at every point
vus_full = []               # Values of Vu (full factored loading)
mus = []

# Initialize at x = 0
x = 0

for i in range(1, no_of_increment+1):
    vu_full = r_a * (a - x) / a
    vu = r_be + ((r_a - r_be) / a) * (a - x)
    mu = (r_a + vu) / 2 * x
    mus.append(mu / 1000 ** 2)

    if (vu * d > mu):
        mu = vu * d

    vc = (1.0 / 7.0) * (math.sqrt(fcPrime) + 120 * p * (vu * d / mu)) * b * d

    xs.append(x / 1000)
    vcs.append(vc / 1000)
    vus.append(vu / 1000)
    simp.append(vc_simplified / 1000)
    beam.append(0)
    vus_full.append(vu_full / 1000)


    x = increment * i

# ----------------------------------------------
# Plotting
# ----------------------------------------------
fig, ax = plt.subplots()
plt.figure(figsize=(10,8))
plt.title("Shear Equation for Beams")
plt.xlabel('Distance, x in meters')
plt.ylabel('Concrete Shear Capacity, Vc in kN')
plt.grid()

axis, = plt.plot(xs, beam, ':', color='red')
detailed, = plt.plot(xs, vcs, label='Detailed')
simplified, = plt.plot(xs, simp, label='Simplified')
vu, = plt.plot(xs, vus, '-', label='Vu (Envelop)', color='red')
vu_full, = plt.plot(xs, vus_full, '--', label='Vu (Full factored loading)', color='magenta')
## moments, = plt.plot(xs, mus, label='Mu', color='gray')
plt.legend(handles=[axis, detailed, simplified, vu, vu_full], loc='best', fontsize=14)

# ----------------------------------------------
# Annotation
# ----------------------------------------------
# Texts
v_envelope_text = "Vu envelop @" + "(" + str(a / 1000) + ")" + " = " + str(r_be / 1000) + \
                    "\nVu = " + str(r_be / 1000)
v_full_text = "Vu for full \nfactored loading"
v_max_text = "Vu(max) = " + str(r_a / 1000)
text_detailed = "Vc using \ndetailed method"
text_simplified = "Vc using \nsimplified method"
text_rho = u'\u03C1' + " = " + str(round(As / (b * d), 4))

# Points
pt_detailed = (a / 1000 / 2, vcs[int(no_of_increment / 2)])
pt_simplified = (a / 1000 / 3, simp[int(no_of_increment / 3)])
pt_vu_full = (3, 350)

plt.text(0, 10, text_rho, fontsize=16)
plt.text(a / 1000, r_be / 1000, v_envelope_text)
plt.text(0, r_a / 1000, v_max_text)
plt.annotate('Straight line approximation \nof maximum shear envelop Vu \ndue to factored live load',
             xy=(2, 200), xytext=(3, 250),
            arrowprops=dict(arrowstyle='->', color='green'),
            horizontalalignment='right', verticalalignment='top')
plt.annotate(text_detailed, xy=pt_detailed, xytext=(a / 1000 / 3, 100),
             horizontalalignment='right', verticalalignment='top',
             arrowprops=dict(arrowstyle='->', color='green'))
plt.annotate(text_simplified, xy=pt_simplified, xytext=(a / 1000 / 3, 400),
             horizontalalignment='right', verticalalignment='top',
             arrowprops=dict(arrowstyle='->', color='green'))
plt.annotate(v_full_text, xy=(a / 1000 / 2, r_a / 1000 / 2), xytext=pt_vu_full,
             horizontalalignment='right', verticalalignment='top',
             arrowprops=dict(arrowstyle='->', color='green'))

plt.fill_between(xs, simp, vcs, hatch='/', facecolor='none')

plt.show()

# ----------------------------------------------
# Comparison
# ----------------------------------------------
