#### I. Problem 2: Shear

1. Plot the shear equation for beams (Detailed and Simplified) considering a simple beam problem.

2. Compare the two plots according to its area of influence. State which is more conservative and economical.

3. Compute the maximum  ultimate load the beam can resist for shear considering 
   - minimum shear reinforcement
   - maximum shear reinforcement



#### II. Solution:

1. Simplified Method
   $$
   V_c = \dfrac{1}{6} \sqrt{f'c} b_w d
   $$

2. Detailed Method
   $$
   V_c = \dfrac{1}{7} \{\sqrt{f'c} + 120\rho_w \dfrac{V_u d}{M_u}\}b_wd
   $$



Assuming the beam is given below:

| Property | Value | Unit   |
| -------- | ----- | ------ |
| $b$      | 375   | $mm$   |
| $d$      | 570   | $mm$   |
| $As$     |       | $mm^2$ |
| $f'c$    | 27.6  | $MPa$  |
| $fy$     | 275   | $MPa$  |

![](figures/beam-loading.JPG)



#### Using python for calculations:

```python
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
```

```python
# ----------------------------------------------
# Constants / Factors
# ----------------------------------------------
dl_factor = 1.2             # Deadload factor
ll_factor = 1.6             # Liveload factor
```

```python
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

# Initialize at x = 0
x = 0

for i in range(1, no_of_increment+1):
    vu_full = r_a * (a - x) / a
    vu = r_be + ((r_a - r_be) / a) * (a - x)
    mu = (r_a + vu) / 2 * x

    # Fraction Vu.d/Mu should not exceed unity
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
```

Plot of the equations:

![](figures/Figure_2.png)