# Python code giving the design calculations for the
# quick-and-dirty noise source.

from sympy import symbols, solve

# KNOWN VALUES

# 3 resistor values (see schematic)
R1, R2, R3 = symbols('R1 R2 R3')

# Forward voltage drop of the B-E junction of Q2
Vdrop = symbols('Vdrop')

# Reverse avalanche voltage of the B-E junction of Q1
Vzener = symbols('Vzener')

# Positive power supply voltage
Vcc = symbols('Vcc')

# Current gain of Q2
beta = symbols('beta')

# UNKNOWN VALUES

# DC voltages, currents 
V_A, V_B, V_C, V_D = symbols('V_A V_B V_C V_D')
I_R1, I_R2 = symbols('I_R1 I_R2')

# Base current of Q2 is just I_R1 because there's no other path for it to flow
# I_R2 is alpha*I_R3 but alpha is close enough to 1 to ignore

# UNCOMMENT THE NEXT LINES TO PROVIDE SPECIFIC VALUES

# Vcc = 12.0
# Vdrop = 0.7
# Vzener = 7.0
# beta = 160.0
# R1 = 680.0e3
# R2 = 4.7e3
# R3 = 1.0e3

# Solve equations to give the calculation/solution

constraints = [
    (Vcc - V_A) - (I_R1 * R1),    # Ohm's Law, R1
    (V_A - V_B) - Vzener,         # Zener voltae
    (V_B - V_C) - Vdrop,          # Diode drop
    (Vcc - V_D) - (I_R2 * R2),    # Ohm's Law, R2
    V_C - (I_R2 * R3),            # Ohm's Law, R3
    I_R2 - beta * I_R1,           # Transistor h_FE
]
unknowns = [I_R1, I_R2, V_A, V_B, V_C, V_C, V_D]
solns = solve(constraints, unknowns, dict=True)

# Print the values we found

for s in solns:
    for v, val in s.items():
        print(f'{v} = {val.simplify().factor()}')

    
    



