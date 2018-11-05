Mu = 630540             # Moment to be resisted
Mu_calculated = 0.0     # Calculated Mu during iteration
Af = 0                  # Area of steel to be solved
phi = 0.75              # Reduction factor for shear
fy = 40000              # Steel tensile strength
fc_prime = 3000         # Concrete compressive strength
d = 15.5                # Effective depth of corbel
b = 12                  # Corbel thickness

while (Mu_calculated < Mu):
    a = Af * fy / (0.85 * fc_prime * b)             # Height of rectangular compression block
    Mu_calculated = Af * phi * fy * (d - (a / 2.0))
    Af += 0.001                                     # Af iteration

print(Af)