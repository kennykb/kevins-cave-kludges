# Compute resistor values for the triangle-wave oscillator
# Copyright © 2024 by Kevin B. Kenny
#
# See the file 'LICENSE' in the containing directory for the
# terms and conditiopns on hte use of this script, and a
# DISCLAIMER OF ALL WARRANTIES.

import bisect
from math import log10
import numpy as np
from sympy import symbols, solve

########################################################################
#
# Code to find a pair of E24 components in a given ratio of values.
#
########################################################################

# E24 standard values, such as are used for 5% tolerance components

e24 = np.array([1.0, 1.1, 1.2, 1.3, 1.5, 1.6,
                1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1,
                5.6, 6.2, 6.8, 7.5, 8.2, 9.1,
                10.0], dtype=np.float32)

def find_e24_value_pair(v2_over_v1, min_v1):

    '''
    Finds a pair of E24 values v1 and v2,
    where the ratio v2/v1 is as close as possible to v2_over_v1,
    with v1 constrained to lie between min_v1 and 10*min_v1
    '''
    
    # Split min_v1 into a power of 10 times a significand between 1 and 10
    min_v1_char = int(np.floor(log10(min_v1)))
    min_v1_decade = 10.0**min_v1_char
    min_v1_significand = min_v1 / min_v1_decade

    # Find the E24 value less than min_v1
    v1ind = bisect.bisect(e24, min_v1_significand) - 1

    # Find a range of E24 values between min_v1 and 10*min_v1
    trial = min_v1_decade * np.concatenate((e24[v1ind:-1], 10.0*e24[:v1ind]))

    # Initialize to search for a pair of values with a close ratio
    # to v2_over_v1

    besterr = 1.
    bestv1 = None
    bestv2 = None

    # Iterate over the trial values
    for v1 in trial:

        # Find the exact value of v2 given v1
        v2_nominal = v1 * v2_over_v1

        # Split into significand and power of 10
        v2_char = int(log10(v2_nominal))
        v2_decade = 10.0**v2_char
        v2_significand = v2_nominal / v2_decade

        # Find the E24 values above and below the computed V2 value
        v2ind = bisect.bisect(e24, v2_significand)
        v2lo = e24[v2ind - 1] * v2_decade
        v2hi = e24[v2ind] * v2_decade

        # Find the relative errors produced by the two values
        errlo = (v2_nominal - v2lo) / v2_nominal
        errhi = (v2hi - v2_nominal) / v2_nominal

        # Update best-so-far if we've found a new best.
        if errlo < besterr:
            besterr = errlo
            bestv1 = v1
            bestv2 = v2lo
        if errhi < besterr:
            besterr = errhi
            bestv1 = v1
            bestv2 = v2hi
            
    return bestv1, bestv2


########################################################################

# Parameters for the Buchla-like oscillator

# 12 volt collector voltage
Vcc = 12

# triangle wave 5vpp, 2.5Vpeak
Vtri = 2.5

# Find the logic high voltage
Vout = 2*Vcc*Vtri/(Vcc + Vtri)
print(f'Logic high voltage: {Vout} V')

# Find resistor values for the divider on the integrator output

R2min = 12000
R2, R1 = find_e24_value_pair(Vtri / Vcc, R2min)
print(f'Divider on integrator output: series {R1:.1e} ohm; shunt {R2:.1e} ohm')

# Find resistor ratio for the divider on the comparator output
r4_over_r3 = Vout / (Vcc - Vout)

# Find good values for that ratio
R3min = 12000
R3, R4 = find_e24_value_pair(r4_over_r3, R3min)
print(f'Divider on comparator output: pull-up {R3:.1e} ohm; pull-down {R4:.1e} ohm')

# Find resistor ratio for divider on switch
half_Vout = 0.5 * Vout
r6_over_r5 = half_Vout / (Vcc - half_Vout)

# Find good values for that resistor pair
R5min = 47000
R5, R6 = find_e24_value_pair(r6_over_r5, R5min)
print(f'Divider on switch: pull-up {R5:.1e} ohm; pull-down {R6:.1e} ohm')

