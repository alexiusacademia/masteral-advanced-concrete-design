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

***Figure 1: Given section***

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

***Figure 2: Moment Capacity vs. Steel Reinforcement relationship curve*** 

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notebooks\Problem Set 2\output_3_1.png)

Also, a snippet of the resulting table of calculated $As$ and $Mn$ is shown below showing the transition between the steel yielding and not yielding.

***Figure 3: Snippet of case 4 results***

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notebooks\Problem Set 2\Result_snippet.png)

Note that the snippet above is part of the **Case 4** of this problem.



### IV. Comments/Observations

---

Following are comments and findings in this problem set.

- Case 1 and 3 shows nearly same amount of Moment Capacity despite having different values of $fy$. It can be noted though that the one with greater $fy$ (Case 3), reaches its max moment with less steel area ($As$). Similar is true with Case 2 and 4.
- For each case, it can be noted that at a specific point, each curve changed its slope abruptly, from steep to almost flat. This point is the transition between under and over reinforced or at balanced steel reinforcement. Numerical data for this point is also presented in the ***figure 2*** above. Beyond this point, is where the concrete yields at strain of 0.003 and steel no longer reaches its yield strength.
- It was also observed that when steel no longer yields, moment capacity doesn't increase much with respect to steel even if we increase its area significantly. This is observed in the part of each curve with small slope.




### V. Appendix

---

##### References

- Gillesania, DI T., *Simplified Reinforced Concrete Design*, Diego Innocencio Tapang Guillesania, 2013
- American Concrete Institute, *Building Code Requirements for Structural Concrete (ACI 318-95) and Commentary (ACI 318R-95)*, 1995
- Nilson, A. H., Darwin, D., Dolan, C. W., *Design of Concrete Structures 14th ed.*, McGraw-Hill, 2010, Retrieved from http://www.engineeringbookspdf.com





##### Source Code

The programming language used in this problem set is **Python3** with the help of **Jupyter Notebook** for presenting the result. The full source code used is shown below. This source code is also available at github (https://github.com/alexiusacademia/masteral-advanced-concrete-design/blob/master/Notebooks/Problem%20Set%202.ipynb)

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import math

def centroid_of_tbeam(bf, tf, bw, y):
    # Calculate centroid of t-beam from top of flange
    # y - height of beam
    kd_prime = 0
    if (y <= tf):
        kd_prime = y / 2
    else:
        a_total = bf * tf + bw * (y - tf)
        ay = bf * tf * tf / 2
        ay += bw * (y - tf) * ((y - tf) / 2 + tf)
        kd_prime = ay / a_total
    return kd_prime

def area_of_tbeam(bf, tf, bw, y):
    # Calculate the area of t-beam
    area = 0
    if (y <= tf):
        area = bf * y
    else:
        area = bf * tf + bw * (y - tf)
    return area

student_number = [3, 3, 8]
d = 435
bw = 250
tf = 125
ϵcu = 0.003
Es = 200000
fc_base = 28        # Basis for calculating β1
student_number_reversed = ['.']

# Reverse the student number then append decimal at the start
for i in range(len(student_number)):
    student_number_reversed.append(str(student_number[len(student_number) - 1 - i]))

# Converted student number
student_number_reversed = float(''.join(student_number_reversed))

# Factor for calculating flange width
α = 10 + 10 * student_number_reversed

# Calculate for b then round to the nearest 25mm
bf = bw + α * tf
bf = int(round(bf / 100 * 4) / 4 * 100)
print('bf = ', bf)
# Given arrays
fcPrime = [20, 40, 20, 40]
fy = [300, 300, 400, 400]
β1 = []

# Calculate for corresponding β1
for fcx in fcPrime:
    if fcx <= fc_base:
        β1.append(0.85)
    else:
        β1.append(round(0.85 - (0.05 / 7)*(fcx - fc_base), 3))
        
# Results array
M = ([0], [0], [0], [0])
As = ([0], [0], [0], [0])
MnMax = []
        
# -------------------------------------
# Start of problem main calculation
# -------------------------------------
for i in range(4):     # 4 cases
    print('= = = = = = = = = = = = =')
    print('Case # ', i+1)
    print('= = = = = = = = = = = = =')
    
    # Calculate balanced value for 'c'
    c_bal = 600 * d / (600 + fy[i])
    
    # Balanced equivalent compression block height
    a_bal = β1[i] * c_bal
    
    # Web component of the compression, z
    z_bal = a_bal - tf if a_bal > tf else 0
    
    # Balanced equation
    # Asb.fy = 0.85 f'c.bf.tf + 0.85f'c.bw.z
    As_bal = (0.85 * fcPrime[i] * bf * tf + 0.85 * fcPrime[i] * bw * z_bal) / fy[i]
    
    print('cb = ', c_bal, 'ab = ', a_bal, 'zb = ', z_bal, 'Asb = ', round(As_bal, 3))
    
    As_limit = 2 * As_bal
    
    As_trial = 100
    Mmax = 0.0
    while (As_trial <= As_limit):
        a = 10
        c = a / β1[i]
        As_calc = 0
        fs = 0.0
        fs_actual = 0.0
        steel_yields = False
        while (As_calc < As_trial):
            c = a / β1[i]
            fs = 600 * (d - c) / c
            fs_actual = fs
            if (fs >= fy[i]):
                fs = fy[i]
                steel_yields = True
            Ac = area_of_tbeam(bf, tf, bw, a)
            
            As_calc = 0.85 * fcPrime[i] * Ac / fs
            # Try for a
            a += 0.02
        
        # Calculate for the strain in concrete
        ϵc = (fs/Es) / (d-c) * c
        
        # Calculate moment
        Mn = As_calc * fs * (d - centroid_of_tbeam(bf, tf, bw, a))
        Mmax = Mn
        M[i].append(Mn/1000**2)
        As[i].append(As_calc)
        
        print('As = ', round(As_trial, 2),'M = ', round(Mn / 1000**2, 2), 'c = ', \
              round(c, 2), 'a = ', round(a, 2), 'fs = ', round(fs, 2), 'fs (actual) = ', fs_actual,
             'ϵc = ', ϵc)
        # Increment steel area each loop
        As_trial += 100
        
    MnMax.append(Mmax)
    
# Plot the curves
plt.figure(figsize=(10,8))
plt.title("Moment-Capacity Curve", fontsize=20)
plt.xlabel(r'$A_s mm^2$', fontsize=16)
plt.ylabel('Moment  in kN-m', fontsize=16)
plt.grid()

# Plot the converted values
case1, = plt.plot(As[0], M[0], label='Case 1: fc\'= '+ str(fcPrime[0]) + ' fy = ' +\
                  str(fy[0]) + 'Mn Max = ' + str(round(MnMax[0]/1000**2,2)), color='blue')
case2, = plt.plot(As[1], M[1], label='Case 2: fc\'= '+ str(fcPrime[1]) + ' fy = ' +\
                  str(fy[1]) + 'Mn Max = ' + str(round(MnMax[1]/1000**2,2)), color='purple')
case3, = plt.plot(As[2], M[2], label='Case 3: fc\'= '+ str(fcPrime[2]) + ' fy = ' +\
                  str(fy[2]) + 'Mn Max = ' + str(round(MnMax[2]/1000**2,2)), color='orange')
case4, = plt.plot(As[3], M[3], label='Case 4: fc\'= '+ str(fcPrime[3]) + ' fy = ' +\
                  str(fy[3]) + 'Mn Max = ' + str(round(MnMax[3]/1000**2,2)), color='red')

def func(x, pos):  # formatter function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

y_formatter = tkr.FuncFormatter(func)
x_formatter = tkr.FuncFormatter(func)

ax = plt.subplot(111)
ax.yaxis.set_major_formatter(y_formatter)
ax.xaxis.set_major_formatter(x_formatter)

plt.legend(handles=[case1, case2, case3, case4], loc='best', fontsize=14)
plt.show()
```






