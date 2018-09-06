# Advanced Design of Reinforced Concrete



### Chapter 1: Introduction, Materials and Properties



#### 1.1 Reinforced Concrete Structures

Reinforced concrete is the union of two materials, <u>plain concrete</u> and <u>steel bars</u>.

*<u>Plain concrete</u>* - possesses high compressive strength but little tensile strength.

*<u>Steel bars</u>* - embedded in the concrete which provides the needed tensile strength.

Steel bars are also often used in compression zone of concrete to provide an added compressive strength to the beam.



##### 1.1.1 Reasons why steel and concrete work readily:

1. Bond - prevents slip of the bars relative to concrete.
2. Proper concrete mixture - provides adequate impermeability against water and bar corrosion.
3. Similar rates of thermal expansion:
   1. Concrete - 0.000010 to 0.000013 $^\circ$C
   2. Steel - 0.000012 $^\circ$C

> Transverse cracks may appear near the steel bars in tension (unless prestressed), such cracks are expected.



#### 1.2 Plain Concrete

Plain concrete is made by mixing cement, fine aggregates, coarse aggregate, water and sometimes, admixtures.

The strength of concrete depends on many factors:

- proportion of the ingredients
- conditions of temperature
- moisture under which it is placed and cured



#### 1.3 Cement

Cement is a material that has adhesive and cohesive properties. These enables mineral fragments to bond and form a solid mass.

##### 1.3.1 Portland cement

- usual hydraulic cement used in reinforced concrete. Concrete used with this attains adequate strength at <u>**14 days**</u> so that forms can be removed and reaches its design strength at **<u>28 days</u>**.

##### Table 1.3.1 Types of Portland Cement

| Type | Uses                                                         |
| ---- | ------------------------------------------------------------ |
| I    | Ordinary construction, special properties are not desired    |
| II   | Ordinary construction, moderate sulfate resistance or moderate heat of hydration is desired |
| III  | When high early strength is desired                          |
| IV   | When low heat of hydration is desired                        |
| V    | When high sulfate resistance is desired                      |



#### 1.4 Aggregates

Occupies about 75% of the total volume of concrete. 

##### 1.4.1 Normal Weight Concrete

Normal stone aggregates makes the concrete weighs about $2,300 kgs/m^3$. Adding of steel reinforcement, unit weight of concrete for the purpose of calculation is $2,400 kgs/m^3$.

##### 1.4.2 Lightweight Structural Concrete

Lightweight concrete have aggregates made of expanded clays and shales and weighs about $1,120$ to $1,840 kgs/m^3$



#### 1.5 Admixtures

##### 1.5.1 Air Entraining Admixtures

Causes air in the form of bubble (about 1mm $\phi$) to form throughout the concrete to increase workability and resistance to deterioration.

##### 1.5.2 Accelerating Admixtures

Accelerate the rate of early age strength development.

##### 1.5.3 Water-reducing and Set-controlling Admixtures

Improve the fresh and hardening of concrete. This reduces the water cement ratio while decreasing the use of cement and increasing strength.

##### 1.5.4 Admixture for Flowing Concrete

Used in concrete with high volume placement such as slabs, mats and pavements.



#### 1.6 Compressive Strength

The strength of concrete is dependent on the mixture of cement, aggregates, water and sometimes admixtures. 

***<u>Reference Concrete Strength</u>*** - uniaxial compressive strength measured from cylinder compression tests.

The most important variable in determining concrete strength is the <u>water-cement ratio</u>. The lower the ratio, the higher the compressive strength.

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notes\Figure1-Water-Cement-Ratio.PNG)

Nearly all reinforced concrete behavior is related to the 28-days compressive strength, $f'c$. Note that this still depends on the size and shape of the test specimen. In normal weight concrete, in average, the 6 x 12in  cylinder is 80% of the 150-mm cube strength and 83% of the 200-mm cube strength.



#### 1.7 Tensile Strength

Tensile strength property of concrete greatly affects the size and extent of cracks in structures.

Test in this property is usually done using split-cylinder test by placing the cylinder on its side then applying the load. The split-cylinder test result has been found to be proportional to $\sqrt{f'c}$:

Modulus of rupture, $fct = 0.5\sqrt{f'c}$        to       $0.6\sqrt{f'c}$               (for normal weight concrete)  in $MPa$

Note that test result for modulus of rupture and the one calculated from $fr = \dfrac{Mc}{I}$ are different. The computed gives higher values due to compressive strength distribution is not linear when tensile failure is imminent. 



#### 1.8 Modulus of Elasticity

Modulus of elasticity of concrete varies with strength, unlike that of steel. For normal weight concrete, ACI-8.5.1 suggests
$$
Ec = 57,000\sqrt{f'c}
$$
where Ec is in psi, and roughly
$$
Ec = 4,700\sqrt{f'c}
$$
where Ec is in MPa (ACI 318-05M).

![](D:\Personal\Masteral\AdvancedConcreteDesign\Notes\Figure2-Concrete-Stress-STrain-Curve.PNG)



#### 1.9 Creep and Shrinkage

Properties of concrete that are hard to predict and is time-dependent. These becomes hard to predict because of inaccuracies and lots of unknown variables.

##### 1.9.1 Creep

Creep is the property by which a material continues to deform with time under sustained loading. Factors affecting creep are composition of cement, admixture and sizes of aggregates, water-cement ratio, closing of internal voids and flow of water out of cement during drying.

##### 1.9.2 Shrinkage

Volume change of concrete during hardening and curing. This may be controlled by continuously wetting or watering the structure during curing period. 





### Chapter 2: Design Methods and Requirements

#### 2.1 Design Code

Varies depending on country. These codes must be adopted by a governing body to be legal.



#### 2.2 Working Stress Design Method

A structure is designed so that the resulting stress in an element do not exceed a specified allowable stress. This may be expressed by the following expression:
$$
f \leq f_{allow}
$$
where:

$f = $ an elastic stress calculated, for example by, $f = \dfrac{M_c}{I}$

$f_{allow} = $ a predefined allowable stress given by a design code.



##### 2.2.3 Obstacles on WSD Method

1. No simple way to account for different degrees of uncertainty of various kinds of loads.
2. Creep and shrinkage are not easily accounted for by calculation of elastic stress.
3. Concrete stress is not proportional to strain up to its crushing point.



#### 2.3 Strength Design Method

Also called *Ultimate Strength Design (USD)* method or *Load Resistance Factor Design (LRFD)*.

The service loads are increased by factors to obtain load at which failure is considered imminent. The resulting loads are called *factored loads*.

The resulting stress in the structure is then proportioned such that strength is reached when factored loads are acting and can be expressed by:
$$
strength\ provided \geq strength\ required
$$
where:

$strength\ provided = $ computed in accordance to provisions of a building/structural code.

$strngth\ required = $ computed using structural analysis.





### Chapter 3: Strength of Rectangular Sections in Bending

#### 3.1 Flexural Behavior and Strength of Rectangular Sections

<figure>
    <img src="D:\Personal\Masteral\AdvancedConcreteDesign\Notes\images\Simple Beam.jpg" width="600" caption="test"/>
    <figcaption>Figure 3.1: Simply supported beam with concentrated loads</figcaption></figure>

On a section in Figure 3.1, flexure-induced stresses will cause compression at the top and tension at the bottom. Concrete, which is strong in compression but weak in tension resists the stresses in compression zone at the top while steel is placed at the bottom of the beam to resist tension stress.

<figure><img src="D:\Personal\Masteral\AdvancedConcreteDesign\Notes\images\Stress Distributions in 3 Stages.jpg"> <figcaption>Figure 3.2: Stress distribution at 3 stages</figcaption></figure>

Figure 3.2 above shows stress distributions of a singly reinforced concrete beam in three (3) different stages of its behavior.

1. Stage 1 (Figure 3.2 - a) - shows linear stress distribution in compression down to tension zone. This is also known as *elastic-uncrack stage*.
2. Stage 2 (Figure 3.2 - b) - shows a nonlinear stress distribution and that neutral axis goes higher towards compression zone. This is known as *elastic-crack stage* where concrete in tension area has already reached its cracking capacity.
3. Stage 3 (Figure 3.2 - c) - neutral axis has moved higher as cracks at the bottom grows. This is also the *inelastic stage*.



##### Basis of Nominal Strength

<figure><img src="D:\Personal\Masteral\AdvancedConcreteDesign\Notes\images\BeamStressDiagram.jpg" /><figcaption>Figure 3.3: Beam Nominal Stress Diagram</figcaption></figure>

On the diagram shown above,

| Symbol          | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| $\epsilon_{cu}$ | crushing strain of concrete                                  |
| $\epsilon_s$    | strain at steel tension                                      |
| $d$             | effective depth of beam                                      |
| $b$             | width of the beam section                                    |
| $kd$            | the distance from neutral axis to extreme compression fiber  |
| $Lo$            | the product of constants $k1$ and $k3$                       |
| $As$            | Area of steel reinforcement                                  |
| $fy$            | yield strength of steel                                      |
| $f'c$           | compressive strength of concrete                             |
| $k2$            | shape factor for the stress diagram and dictates the location of compression force resultant based on $kd$ |

Basis:

1. It has been assumed that plane section remains plane after bending up to failure of the beam. This assumption is for homogeneous elastic beams but has also been verified using tests to be good even for cracked, reinforced concrete beams at nominal strength.
2. On average (not true on a local cracked section), it is found that the bond of steel and concrete works well.

The nominal strength of the beam is reached when the strain at the extreme compression fiber reached $\epsilon_{cu}$. And this is when the beam fails.
$$
Mn = As \cdot fy \cdot (d - k2\cdot kd)
$$

$$

$$





#### 3.2 Whitney Rectangular Stress Distribution

<figure><img src="D:\Personal\Masteral\AdvancedConcreteDesign\Notes\images\WhitneyRectangular.jpg" /><figcaption>Figure 3.4: Whitney Equivalent Stress Block</figcaption></figure>

#### 3.3 Design of Section in Bending

##### 3.3.1 Maximum Steel Ratios ($\rho_{max}$):



1. Singly Reinforced Beams
   $$
   \rho_{max} = 0.75\cdot \rho_{bal}
   $$
   This is just a traditional requirement to ensure that steel yields first.

   Note: A more direct way of controlling ductility is to provide maximum value of neutral axis, $kd$. ACI-B.10.3.3 shows that for singly reinforced beams,
   $$
   kd_{max} = 0.75\cdot kd_{bal}
   $$

2. Doubly Reinforced Beams

   For ductility requirements, it is much more appropriate to follow and limit $kd$ to $0.75\cdot kd$.



### Chapter 4: Shear Strength and Shear Reinforcement

Shear failure or *Diagonal Tension* on beams is difficult to predict accurately.

Shear failure may be more catastrophic than flexure failure. A concrete beam without proper design of shear reinforcement could fail and collapse suddenly without any warning. Unlike in flexure, an under reinforced beam will show signs before failure like cracking, large deflections, and so they can be sometimes be applied with corrective measures.

#### 4.1 Methods of Shear Design

##### 4.1.1 Variable Angle Truss Model

##### 4.1.2 Diagonal Compression Field Theory

##### 4.1.3 Modified Compression Field Theory



> Large bending moments reduces the shear force at which diagonal cracks form to roughly half of the value is the moment is zero or nearly zero.

It is evident then that shear at which diagonal cracks are developed depends on ratio of shear force to bending moment.

#### 4.2 Behavior of Diagonally Cracked Beams

1. The crack, once formed, spreads, traversing the entire beam from tension to compression face splitting it in two.

   Because of this, it's a good practice to provide minimum shear reinforcement even if it's not required by calculations as they prevents cracks to grow.

2. Sometimes, diagonal cracks formed and spread up to compression zone then stops and not make it to the compression face. In this case, there is no sudden collapse by this failure.