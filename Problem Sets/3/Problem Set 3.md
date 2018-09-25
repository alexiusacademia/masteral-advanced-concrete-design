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

![](D:\Personal\Masteral\AdvancedConcreteDesign\Problem Sets\3\beam-loading.JPG)



##### Case 1: Simplified Method

$$
V_c = \dfrac{1}{6}\sqrt{27.5}\cdot(375)\cdot(570)
$$

$$
V_c(simplified) =186,819.07N
$$

$V_c$ is uniformly distributed throughout the beam
$$
R_A = \dfrac{150 (6)}{2}
$$

$$
R_A = 450 kN
$$

