### I. Problem:

------

Draw the Moment-Capacity and Tension Steel (Mn - As) relationship curve of a reinforced concrete t-beam of different cases with parameters as follows:

**General Cases**

| Cases  | fc'  | fy   |
| ------ | ---- | ---- |
| Case 1 | 20   | 300  |
| Case 2 | 30   | 300  |
| Case 3 | 20   | 400  |
| Case 4 | 30   | 400  |

**Beam Properties**

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notebooks\Problem Set 2\T-Beam.jpg)

| Property                                            | Value                | Unit |
| --------------------------------------------------- | -------------------- | ---- |
| f'c                                                 | [20, 40, 20, 40]     | MPa  |
| fy                                                  | [300, 300, 400, 400] | MPa  |
| Effective depth (d)                                 | 435                  | mm   |
| Web width (b~w~)                                    | 250                  | mm   |
| Thickness of flange (t~f~)                          | 125                  | mm   |
| $\epsilon$~cu~                                      | 0.003                |      |
| E~s~                                                | 200,000              | MPa  |
| f'c reference                                       | 28                   | MPa  |
| Student number (last 3-digits)                      | 338                  |      |
| Factor based of on reversed student number $\alpha$ | 0.833                |      |
| $bf = bw + \alpha \cdot tf$                         | 2550                 | mm   |

$\beta 1$ is solved for each value of $f'c$.

```python
fcPrime = [20, 40, 20, 40]
fy = [300, 300, 400, 400]
β1 = []
# Calculate for corresponding β1
for fcx in fcPrime:
    if fcx <= fc_base:
        β1.append(0.85)
    else:
        β1.append(round(0.85 - (0.05 / 7)*(fcx - fc_base), 3))
```

$\beta 1$ now is `[0.85, 0.764, 0.85, 0.764]`



### II. Solutions / Methodology

------

#### A. Assumptions

- In this problem, tensile strength of concrete is neglected, so that at $As = 0$, $Mn = 0$.
- Stress block used is the Whitney stress block distribution for simplicity of calculation.

#### B. Solution

The solution to the problem is to solve each cases in one go using programming language **python** by looping through a number of four (4) cases.

1. Create list of arrays to hold values for moments and steel areas for each case:

   ```python
   # With initial values of zeros (0's) for Mn and As for each case
   M = ([0], [0], [0], [0])
   As = ([0], [0], [0], [0])
   ```

2. Now for looping on 4 cases:

2.1. Calculation of balanced steel area, needed for the curve and analysis limit.

   ```python
   for i in range(4):
       c_bal = 600 * d / (600 + fy[i])           # Location of neutral axis
       a_bal = β1[i] * c_bal                     # Equivalent height of rectangular
                                                 #  compression block
       z_bal = a_bal - tf if a_bal > tf else 0   # Web component of compression zone
                                                 #  if a > tf
       As_bal = (0.85 * fcPrime[i] * bf * tf + 0.85 * fcPrime[i] * bw * z_bal) 
                           / fy[i]
       As_limit = 2 * As_bal                     # Limit to be analyzed
       As_trial = 100                            # Start calculating here for As
   ```
2.2. Create a loop that tries for each value of As, then calculates the corresponding moment capacity, Mn until As_limit is reached.

   ```python
   while (As_trial <= As_limit):
       a = 10                                    # Trial for height of stress block
       c = a / β1[i]                             # Neutral axis height (kd)
       As_calc = 0                               # Variable to hold calculated As
                                                 # To be compared with As_trial
   ```

2.3. Find the height of stress block by trial and error

   ```python
   	   while (As_calc < As_trial):
           c = a / β1[i]                         # Neutral axis height (kd)
           fs = 600 * (d - c) / c                # Calculated fs
           if (fs >= fy[i]):                     # Use fy if steel yields
               fs = fy[i]
           Ac = area_of_tbeam(bf, tf, bw, a)     # Calling a function to calculate
                                                 #  area of a given t-beam
           As_calc = 0.85 * fcPrime[i] * Ac / fs # Calculate As by equilibrium
           a += 0.02                             # Increment a with 0.02mm
   ```

2.4. Nominal moment is now then calculated by taking a moment at centroid of stress block

```python
       Mn = As_calc * fs * (d - centroid_of_tbeam(bf, tf, bw, a))
       
       # Add the calculated moment and steel area to the array
       M[i].append(Mn/1000**2)
       As[i].append(As_calc)
```

2.5. To finalize a single loop, trial for steel area is incremented by $100 mm^2$ each time

```python
   As_trial += 100
```



This covers the whole process of the calculation. To add some more observations, some data have been collected and inserted to the actual code, (not shown in the main process above) to understand the result more deeply like; maximum nominal moment, strain at the compression fiber and actual steel stress is also collected to find if steel yields in each loop.



### III. Results / Charts

---

The resulting graph for all cases is shown below:

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notebooks\Problem Set 2\output_3_1.png)

Also, a snippet of the resulting table of calculated $As$ and $Mn$ is shown below showing the transition between the steel yielding and not yielding.

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notebooks\Problem Set 2\Result_snippet.png)

Note that the snippet above is part of the **Case 4** of this problem.

### IV. Comments

---

Following are comments and findings in this problem set.

- The first that I find here is in the chart above, the curve for **Case 1**. It can be seen that it has the smallest curvature. Compared to the curve of **Case 2** which has a smallest amount of tensile reinforcement, shows a gradual change in Moment/Load with a high degree of visibility in change in curvature. The same goes to **Case 3**. This indicates, in my opinion, that they shows ductile behavior. The beams shows a large change in curvature which can be relate to the beams deflection (the larger the angle of curvature, the larger the deflection) while the beam at case 1 shows a brittle behavior. The beam reached its allowable strain of 0.003 in concrete without much change in curvature relative to load. 

- Following the 1st comment, if we look at the table in the Results section at Case 1, we can see that the tensile reinforcements did not yield until the beam failed. This could be the reason why we avoid to have a balanced design or even an over reinforced design for that matter.




### V. Appendix

---

##### References

- Gillesania, DI T., *Simplified Reinforced Concrete Design*, Diego Innocencio Tapang Guillesania, 2013
- American Concrete Institute, *Building Code Requirements for Structural Concrete (ACI 318-95) and Commentary (ACI 318R-95)*, 1995
- Nilson, A. H., Darwin, D., Dolan, C. W., *Design of Concrete Structures 14th ed.*, McGraw-Hill, 2010, Retrieved from http://www.engineeringbookspdf.com





##### Source Code

The programming language used in this problem set is **Python3** with the help of **Jupyter Notebook** for presenting the result. The full source code used is shown below. This source code is also available at github (https://github.com/alexiusacademia/masteral-advanced-concrete-design/blob/master/Notebooks/Problem%20Set%201.ipynb)

```python
# Imports
import math
import matplotlib.pyplot as plt

# Define parameters
b = 300                             # Beam width
h = 450                             # Beam height
clearance = 50                      # Clearance from tension steel to bottom of concrete
d = h - clearance                   # d - Effective depth
d_prime = 50                        # d' - Distance from compression steel to concrete compression fiber
fcprime = 21                        # f'c - Concrete compressive strength
fy = 275                            # fy - Steel tensile strength
fr = 0.7 * math.sqrt(fcprime)       # Modulus of fructure
Es = 200000                         # Modulus of elasticity of steel
Ec = 4700 * math.sqrt(fcprime)      # Modulus of elasticity of concrete
β1 = 0.85                           # Beta
η = Es / Ec                         # Modular ratio

# As balance
ρb = (0.85 * fcprime * β1 * 600) / (fy * (600 + fy)) # Balance concret-steel ratio
Asb = ρb * b * d                    # As balance

# Cases
As = [Asb, 0.5*Asb, Asb]       # Tension reinforcements
AsPrime = [0.0, 0.0, 0.5*Asb]      # Compression reinforcements

# Data holders
M = ([], [], [])                    # Array of moments for the 3 cases
ϕ = ([], [], [])                    # Array of curvature for the 3 cases
I = ([], [], [])                    # Array of all computed moment of inertias
kd = ([], [], [])                   # Array of values of neutral axis to compression fiber
fsm = ([], [], [])                  # Array of strains in concrete
yield_pts = []
```


```python
# =========================================
# Utilities
# =========================================
def solveLo(case_no, 𝜆):
    if case_no ==1:
        return 0.85 / 3 * 𝜆 * (3 - 𝜆)
    else:
        return 0.85 * (3*𝜆 - 1) / (3 * 𝜆)
```


```python
# Insert initial values for moment and curvature
for i in range(3):
    M[i].append(0.0)
    ϕ[i].append(0.0)

for i in range(3):
    # =========================================== #
    # Calculation before cracking                 #
    # =========================================== #
    # Calculate for kd of each case
    At = b * h                                          # Concrete alone
    At += (η-1) * As[i]                                 # Concrete plus transformed tension steel
    At += (η-1) * AsPrime[i]                            # Plus transformed compression steel
    Ma = (b * h) * (h / 2)                              # Moment of area of concrete to compression fiber
    Ma += (η-1) * As[i] * d                             # Moment of tension reinf. to compression fiber
    Ma += (η-1) * AsPrime[i] * d_prime                  # Moment of compression reinf. to compression fiber
    kdCalculated = Ma / At
    kd[i].append(kdCalculated)                          # Insert to list of kd

    # Calculate for moment of inertia of each case
    Ic = (b * kdCalculated**3 / 12) + (b * kdCalculated * (kdCalculated / 2)**2)
    Ic += (b * (h - kdCalculated)**3 / 12) + (b * (h - kdCalculated) * ((h - kdCalculated) / 2)**2)
    Ic += (η-1) * As[i] * (d - kdCalculated)**2
    Ic += (η-1) * AsPrime[i] * (kdCalculated - d_prime)**2
    I[i].append(Ic)                                     # Insert to list of I
    
    # Calculate the cracking moment
    Mcr = fr* Ic / (h - kdCalculated)                   # Cracking moment
    M[i].append(Mcr)                                    # Insert to list of M
    
    # Calculate the curvature
    ϕc = fr / (Ec * (h - kdCalculated))                 # Curvature right before cracking
    ϕ[i].append(ϕc)                                     # Insert to list of ϕ
    
    # =========================================== #
    # Calculation after cracking                  #
    # =========================================== #
    # Finding the neutral axis using equilibrium of moment of areas
    # b(kd)(kd/2) + (n-1)As'(kd-d') = nAs(d-kd)
    # -- solve the quadratic equation
    qa = b
    qb = 2 * ((η-1) * AsPrime[i] + η * As[i])
    qc = -2 * ((η-1) * AsPrime[i] * d_prime + η * As[i] * d)
    qd = (qb**2) - (4 * qa * qc)                        # Discriminant
    kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa) # Neutral axis after cracking
    kd[i].append(kdCalculated)
    
    # Calculate moment of inertia
    Ic = (b * kdCalculated**3 / 12) + (b * kdCalculated * (kdCalculated / 2)**2)
    Ic += (η) * As[i] * (d - kdCalculated)**2
    Ic += (η-1) * AsPrime[i] * (kdCalculated - d_prime)**2
    I[i].append(Ic)
    
    # Calculate the curvature
    ϕc = M[i][1] / (Ec * Ic)                            # Curvature right after cracking
    
    M[i].append(Mcr)
    ϕ[i].append(ϕc)
    
    # =========================================== #
    # Calculation at yield point                  #
    # =========================================== #
    fc = 0.5 * fcprime
    ⲉc = fc / Ec
    
    qa = 0.5 * fc * b
    qb = (Es * ⲉc) * (AsPrime[i] + As[i])
    qc = -(Es * ⲉc) * (AsPrime[i] * d_prime + As[i] * d)
    qd = (qb**2) - (4 * qa * qc)           # Discriminant
    kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)

    fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
    fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
    if fs > fy:
        fs = fy

    if fsPrime > fy:
        fsPrime = fys
            
    Mc = 0.5 * fc * b * kdCalculated * (d - kdCalculated / 3) +\
                AsPrime[i] * fsPrime * (d - d_prime)
    ϕc = ⲉc / kdCalculated
    
    M[i].append(Mc)
    ϕ[i].append(ϕc)
    
    yield_pts.append((ϕc*1000, Mc / 1000**2))
    
    # =========================================== #
    # Calculation at inelastic behaviour          #
    # =========================================== #
    # Calculate for ⲉo
    ⲉo = 2 * 0.85 * fcprime / Ec		# This is overridden below
    
    # Iterator increment
    iterator_increment = 0.0002
    
    # For 0 < ⲉc < ⲉo
    ⲉc = 0.5 * ⲉo                       # To override above ⲉo

    # For case 0 < ⲉc < ⲉo
    while (ⲉc + iterator_increment) <= ⲉo:
        ⲉc = ⲉc + iterator_increment
        𝜆o = ⲉc / ⲉo
        k2 = 1 / 4 * (4 - 𝜆o) / (3 - 𝜆o)
        Lo = solveLo(1, 𝜆o)
        fc = 0.85 * fcprime * (2 * 𝜆o - 𝜆o**2)
        kdCalculated = (As[i] - AsPrime[i]) * fy / (Lo * fc * b)
        fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
        fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
        
        if fs >= fy:                                    # Tension steel yields
            # Solve for the stress in compression steel
            if fsPrime < fy:                           
                # Compression steel does not yields
                qa = Lo * fc * b
                qb = (Es * ⲉc) * AsPrime[i] - As[i] * fy
                qc = -(Es * ⲉc) * AsPrime[i] * d_prime
                qd = (qb**2) - (4 * qa * qc)           # Discriminant
                kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
                fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
                fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
            else:
                # fs and fs' > fy
                kdCalculated = (As[i] - AsPrime[i]) * fy / (Lo * fc * b)
                fs = fy
                fsPrime = fy
        else:
            qa = Lo * fc * b
            qb = AsPrime[i] * fy + As[i] * Es * ⲉc
            qc = -As[i] * Es * ⲉc * d
            qd = (qb**2) - (4 * qa * qc)           # Discriminant
            kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
            fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
            fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
            
            if fsPrime < fy:
                # Compression syeel did not yield
                # Compression steel does not yields
                qa = Lo * fc * b
                qb = (Es * ⲉc) * (AsPrime[i] + As[i])
                qc = -(Es * ⲉc) * (As[i] * d + AsPrime[i] * d_prime)
                qd = (qb**2) - (4 * qa * qc)           # Discriminant
                kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
                fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
                fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
        
        Mc = Lo * fc * b * kdCalculated * (d - k2 * kdCalculated) +\
                AsPrime[i] * fsPrime * (d - d_prime)
        ϕc = ⲉc / kdCalculated
        
        M[i].append(Mc)
        ϕ[i].append(ϕc)
        
    # For case ⲉo < ⲉc < ⲉcu
    ⲉc = ⲉo + 0.0001
    while (ⲉc + iterator_increment) <= 0.003:
        ⲉc = ⲉc + iterator_increment
        ζc = ⲉo / ⲉc
        𝜆o = 1 / ζc
        Lo = solveLo(2, 𝜆o)
        k2 = (6 * 𝜆o**2 - 4 * 𝜆o + 1) / (4 * 𝜆o * (3 * 𝜆o - 1))
        fc = 0.85 * fcprime
        kdCalculated = (As[i] - AsPrime[i]) * fy / (Lo * fc * b)
        fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
        fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
        
        if fs >= fy:                                    # Tension steel yields
            # Solve for the stress in compression steel
            if fsPrime < fy:                           
                # Compression steel does not yields
                qa = Lo * fc * b
                qb = (Es * ⲉc) * AsPrime[i] - As[i] * fy
                qc = -(Es * ⲉc) * AsPrime[i] * d_prime
                qd = (qb**2) - (4 * qa * qc)           # Discriminant
                kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
                fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
                fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
            else:
                # fs and fs' > fy
                kdCalculated = (As[i] - AsPrime[i]) * fy / (Lo * fc * b)
                fs = fy
                fsPrime = fy
        else:
            qa = Lo * fc * b
            qb = AsPrime[i] * fy + As[i] * Es * ⲉc
            qc = -As[i] * Es * ⲉc * d
            qd = (qb**2) - (4 * qa * qc)           # Discriminant
            kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
            fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
            fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
            
            if fsPrime < fy:
                # Compression syeel did not yield
                # Compression steel does not yields
                qa = Lo * fc * b
                qb = (Es * ⲉc) * (AsPrime[i] + As[i])
                qc = -(Es * ⲉc) * (As[i] * d + AsPrime[i] * d_prime)
                qd = (qb**2) - (4 * qa * qc)           # Discriminant
                kdCalculated = (-1 * qb + math.sqrt(qd)) / (2 * qa)
                fs = (Es * ⲉc) * (d - kdCalculated) / kdCalculated
                fsPrime = Es * ⲉc / kdCalculated * (kdCalculated - d_prime)
            
        Mc = Lo * fc * b * kdCalculated * (d - k2 * kdCalculated) +\
                AsPrime[i] * fsPrime * (d - d_prime)
        ϕc = ⲉc / kdCalculated
        
        ϕ[i].append(ϕc)
        M[i].append(Mc)
```

```python
# Convert the values of data to smaller figures before plotting
ϕ_converted = ([], [], [])
M_converted = ([], [], [])
for i in range(3):
    for curvature in ϕ[i]:
        ϕ_converted[i].append(curvature * 1000)
    for moment in M[i]:
        M_converted[i].append(moment / 1000**2)
        
# Plot the curves
plt.figure(figsize=(10,8))
plt.title("Moment-Curvature")
plt.xlabel('Curvature  x10^-5 /mm')
plt.ylabel('Moment  in kN-m')
plt.grid()

for yp in yield_pts:
    plt.text(yp[0], yp[1], 'Yield Point')

# Plot the converted values
case1, = plt.plot(ϕ_converted[0], M_converted[0], marker='s', label='Case 1 (As = Asb)')
case2, = plt.plot(ϕ_converted[1], M_converted[1], marker='s', label='Case 2 (As = 0.5Asb)')
case3, = plt.plot(ϕ_converted[2], M_converted[2], marker='s', label='Case 3 (As = 1.2Asb, As\'=0.7Asb)')
plt.legend(handles=[case1, case2, case3], loc='best', fontsize=14)
plt.show()
```




