# Compute the vlaues of resistors needed for the Schmitt trigger
# in the I-V curve tracer.  It's running off a _negative_ power supply!

from sympy import symbols, solve

# The four resistors in the trigger
# R1 - pull-up on the input - to ground
# R2 - pull-down on the input - to -Vee
# R3 - feedback resistor
# R4 - pull-up on the open collector output - to ground
R1, R2, R3, R4 = symbols('R1 R2 R3 R4')

# Voltages:
#    Vh - high trip point
#    Vl - low trip point
#    Vee - negative power supply
#    V_R1  Voltage at top end of R1 - ground
#    V_R2  Voltage at bottom end of R2  - -Vee
#    V_R3  Voltage at top end of R3, assumed to be the same as top of R4
#      (assuming R4 << R3)
Vh, Vl, Vee, V_R1, V_R2, V_R3 = symbols('Vh Vl Vee V_R1 V_R2 V_R3')

#  Symbolic solution

# Equations:  Current in the three resistors sums to zero at
#             both upper and lower trip points

eqns = [(V_R1 - Vh) / R1 + (V_R3 - Vh) / R3 - (Vh - V_R2) / R2,
        (V_R1 - Vl) / R1 + (Vee - Vl) / R3 - (Vl - V_R2) / R2]

solns = solve(eqns, R1, R2, dict=True)

print(''' Solution with R4 << R3:''')
for s in solns:
    for k, v in s.items():
        print(f'{k} = {v.expand().simplify()}')
print('')
      
# Plug in the actual values
    
Vh = -0.05   # trip at -0.05 volts
Vl = -1.0     # trip at -1 volts
V_R1 = 0    # connect the divider between ground
V_R2 = -12  # and -12V
V_R3 = 0    # pull the R4/R3 combination up to ground
Vee = -12   # and down to -12V

# Equations: Currents again sum to zero.  This time, when the output is HIGH,
#            account for the current in R4

eqns = [(V_R1 - Vh) / R1 + (V_R3 - Vh) / (R3 + R4) - (Vh - V_R2) / R2,
        (V_R1 - Vl) / R1 + (Vee - Vl) / R3 - (Vl - V_R2) / R2]

solns = solve(eqns, R1, R2, dict=True)

print('Solution accounting for R4, actual power supplies:')
for s in solns:
    for k, v in s.items():
        print(f'{k} = {v.expand().simplify()}')
print('')

# Size R4 for 2 mA idle current and restate equations with it filled in

R4 = 6200
eqns = [(V_R1 - Vh) / R1 + (V_R3 - Vh) / (R3 + R4) - (Vh - V_R2) / R2,
        (V_R1 - Vl) / R1 + (Vee - Vl) / R3 - (Vl - V_R2) / R2]

solns = solve(eqns, R1, R2, dict=True)

print('Solution with R4 = 6k2:')
for s in solns:
    for k, v in s.items():
        print(f'{k} = {v.expand().simplify()}')
print()

# Choose 33k pretty arbitrarily for R3 and restate equations with it filled in

R3 = 33000
eqns = [(V_R1 - Vh) / R1 + (V_R3 - Vh) / (R3 + R4) - (Vh - V_R2) / R2,
        (V_R1 - Vl) / R1 + (Vee - Vl) / R3 - (Vl - V_R2) / R2]

solns = solve(eqns, R1, R2, dict=True)

print('Solution with R4=6k2, R3=33k')
for s in solns:
    for k, v in s.items():
        print(f'{k} = {v.expand().simplify()}')
