#!/usr/bin/env python

"""
Produce a Bode plot of a speaker's impedance

Copyright © 2026 by Kevin B. Kenny
Please refer to the 'LICENSE.txt' file in the software distribution for
the terms and conditions of reuse, and a DISCLAIMER OF ALL WARRANTIES.


Setup:

FY6900 signal generator connects to the input, as shown in the schematic.
It should be set to a sine wave at 2 Vpp output. Its frequency will be
controlled by this program.

Scope channel 1 monitors the output of the voltage sense amp (TP103
in the schematic).
Scope channel 2 monitors the output of the current sense amp (TP104
in the schematic).

The scope should use an external trigger input to trigger off the
FY6900's sync output (on its rear panel). I used channel 4 for this
input, and added a 50 ohm terminator to clean up some nastiness
in the signal.

The scope's vertical and horizontal scales will be set automatically
according to the test conditions.
"""

import argparse
import csv
from ds1054z import DS1054Z
from fygen import fygen
from math import floor, pi
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import ticker
from time import sleep
import numpy as np
from numpy import cos, exp, floor, log, log10, pi, sin
import sys
from sys import argv

parser = argparse.ArgumentParser\
    (description='Measure a speaker and produce a Bode plot and spreadsheet '
     'of impedance vs frequency.')

parser.add_argument('runName', 
                    default='speaker',
                    type=str,
                    nargs=1,
                    help='Name of the test run.')
parser.add_argument('--start', dest='start_frequency',
                    type=float, default=20.0,
                    help='Starting frequency')
parser.add_argument('--end', dest='end_frequency',
                    type=float, default=20480.0,
                    help='Ending frequency')
parser.add_argument('--steps', dest='frequency_steps',
                    type=int, default=161,
                    help='Number of frequency steps to take')
cmd_args = parser.parse_args()

#----------------------------------------------------------------------
# CONSTANTS

# IP address of DS1054Z scope.
scope_ip = '192.168.2.101'

# USB-serial port communicating with FY6900 function generator
fygen_port = 'COM3'

# Frequency range to plot

start_frequency = cmd_args.start_frequency
end_frequency = cmd_args.end_frequency

# Amplitude of the wave to apply to the test harness (V)

input_amplitude = 5

# Maximum output amplitude expected - usually should be a
# little bit bigger than the supply span

output_amplitude = 40

# Remember scope scales so that we can skip resetting if they don't change

scope_v_scales = [None, None, None, None]

#----------------------------------------------------------------------

def fine_argmax(arr):
    """
    Like np.argmax, but performs parabolic interpolation with two neighouring
    points

    Arguments:
        arr - Array to search

    Results:
        Returns a floating point argmax that interpolates parabolically
        near the maximum value of 'arr'
    """
    coarse = np.argmax(arr)
    ym1 = arr[coarse-1]
    y0 = arr[coarse]
    y1 = arr[coarse+1]
    return coarse + (ym1 - y1)/(2*(ym1 - 2*y0 + y1))


class ScopeFault(Exception):
    '''
    Exception thrown if the oscilloscope reports any error while
    capturing a waveform
    '''
    pass    

def lowlevel_set_ch1_freq(fg, freq):
    """
    Sets channel 1 frequency on the AWG.
    
    The FYGen package sends the frequency without a decimal point.
    The FY6900 appears to expect that it _will_ have a decimal point.

    """
    fg.send(f'WMF{freq:015.6f}')


def stop_scope(scope):
    '''
    Stops the oscilloscope and makes sure that (a) it has had time to stop,
    (b) it actually acted on the 'stop' command.
    '''
    scope.stop()
    while scope.query(':TRIG:STAT?') != 'STOP':
        sleep(0.1)
        scope.stop()

def two_five_ten(x):
    if x <= 2:
        return 2
    elif x <= 5:
        return 5
    else:
        return 10

def set_channel_scale(scope, channel, scale):
    """
    Sets the vertical scale on a channel of the scope if it's changed.

    Arguments:
        scope - Handle to the scope
        channel - Channel number (1-4)
        scale - Vertical scale

    Returns:
        True if the scale has changed, False otherwise
    """
    if scope_v_scales[channel-1] == scale:
        return False
    scope.set_channel_scale(channel, scale)
    return True

def find_scope_v_scale(mn, mx):
    """
    Finds a value to set for 'volts/division' to accommodate the given
    minimum and maximum voltage values (with the scope still set to
    zero offset.

    Arguments:
        mn - Minimum voltage
        mx - Maximum voltage

    Results:
        Returns the desired scale
    """

    larger = max(abs(mn), abs(mx))
    ideal = larger/4 # ideal volts/division
    decade = 10**np.floor(np.log10(ideal))
    retval = decade * two_five_ten(ideal / decade)

    return retval

def find_scope_h_scale(freq):
    '''
    Sets the timebase on the scope to accommodate a given frequency

    Arguments:
        freq - Frequency that will be presented

    Results:
        Returns scale (s / div) and offset (s) 
    '''

    duration = 3 / freq # Total duration we want to display
    ideal = duration/12 # ideal s/divison
    decade = 10**np.floor(np.log10(ideal))
    scale = decade * two_five_ten(ideal/decade)
    offset = 6 * scale

    return scale, offset


def setup(scope, fg):

    """
    Sets up the scope and function generator at the start of a run

    Parameters:
        scope - Handle to the scope
        fg - Handle to the function generator
    """

    stop_scope(scope)

    # scope channel 1 is the input, set its scale

    scale = find_scope_v_scale(-input_amplitude/2, input_amplitude/2)
    set_channel_scale(scope, 1, scale)
    scope.set_channel_offset(1, 0)

    # set up the function generator to supply the correct amplitude
    fg.set(channel=fygen.CH1,
           enable=True,
           wave='sin',
           volts=2,
           offset_volts=0)
    lowlevel_set_ch1_freq(fg, cmd_args.start_frequency)

def reset_scope_v_scale(scope):

    """
    Resets the scope vertical scale to the power supply range in preparation
    for measuring at a single point.

    Arguments:
        scope - Handle to the scope
        output_amplitude - Maximum expected output amplitude

    Returns True if the scope scale changed, False otherwise
    """

    scale = find_scope_v_scale(-output_amplitude/2, output_amplitude/2)
    scope.set_channel_offset(2, 0)
    return set_channel_scale(scope, 2, scale)
    
def setup_one_freq(scope, fg, freq):

    """
    Sets up to take data for a single frequency.

    Arguments:
        scope - Handle to the scope
        fg - Handle to the function generator
        freq - Frequency to set
    """

    stop_scope(scope)
    changed = reset_scope_v_scale(scope)
    scale, offset = find_scope_h_scale(freq)
    scope.timebase_scale = scale
    scope.timebase_offset = offset
    lowlevel_set_ch1_freq(fg, freq)
    sleep(2. / freq + 0.25)
    for i in range(0, 2):
        scope.run()
        sleep(10. / freq + 0.25)
        stop_scope(scope)
        vmin = scope.get_channel_measurement(2, 'vmin')
        vmax = scope.get_channel_measurement(2, 'vmax')
        if vmin is None or vmax is None:
            print('Could not read voltages from scope channel 2')
            raise ScopeFault()
        scale = find_scope_v_scale(vmin, vmax)
        changed = set_channel_scale(scope, 2, scale)
        if not changed:
            break

def analyze_sweep(freq, ts, ins, outs):
    """
    Reduces the data accumulated from the scope at a single frequency

    Arguments:
        freq - Frequency under test
        ts - Time stamps of the oscilloscope values
        ins - Input voltages at the given times
        outs - Output voltages at the given times.

    Returns a tuple (Zbar, phi, R, X) where:
    Zbar is the magnitude of the speaker impedance (ohm)
    phi is the phase angle of the speaker impedance (rad)
    R is the speaker resistance
    X is the speaker reactance.
    """
    N = ts.shape[0] # Number of data points

    time_per_step = (ts[-1] - ts[0]) / (N - 1) # Seconds per time step

    # Find the correlation between an ideal wave of the given
    # frequency and the observed data

    correl = np.correlate(window*outs, window*ins, 'same')

    # The locations of the two peaks in the correlation give the
    # phase delay
    delay_bins = fine_argmax(correl) - 0.5*correl.shape[0]
    time_delay = time_per_step * delay_bins
    phase_angle = time_delay * freq * 2 * pi
    while phase_angle > pi:
        phase_angle -= 2*pi
    while phase_angle < -pi:
        phase_angle += 2*pi

    # The driver has a gain of 0.1. The current sense has a transresistance
    # of 100 V/A
    vls = ins * 0.1;  ils = outs / 100.0

    if delay_bins >= 0:
        # The voltage leads the current by delay_bins observations.
        # Shift the currents earlier in time
        i_indices = np.arange(delay_bins, ils.shape[0], 1.0)
        v_indices = np.arange(0, i_indices.shape[0], 1)
        ils_for_lsq = np.interp(i_indices, np.arange(0, ils.shape[0]), ils)
        vls_for_lsq = vls[0:ils_for_lsq.shape[0]]
                                
    else:
        # The voltage lags the current. Shift the voltages earlier in time
        v_indices = np.arange(-delay_bins, vls.shape[0], 1.0)
        i_indices = np.arange(0, v_indices.shape[0], 1)
        vls_for_lsq = np.interp(v_indices, np.arange(0, vls.shape[0]), vls)
        ils_for_lsq = ils[0:vls_for_lsq.shape[0]]

    A = np.vstack([ils_for_lsq, np.ones(ils_for_lsq.shape[0])]).T
    R, Voff = np.linalg.lstsq(A, vls_for_lsq)[0]
    
    # Return gain/loss and phase lead/lag
    return R, phase_angle, R*cos(phase_angle), R*sin(phase_angle)

def run_sweep(scope, fg, freq):

    """
    Runs the generator and oscilloscope to grab the waveform at a single
    frequency.

    Arguments:
        scope - Handle to the scope
        fg    - Handle to the function generator
        freq  - Frequency for which to acquire the data

    Returns a triple (ts, ins, outs)
        ts - Timestamps at which voltages were acquired
        ins - Input voltages at the given times
        outs - Output voltages at the given times.
    """

    print(f'Ready to take one waveform at freq={freq}')
    setup_one_freq(scope, fg, freq)
    scope.run()
    sleep(10.0/freq + 0.25)
    scope.stop()
    ts = np.float32(scope.waveform_time_values)
    ins = np.float32(scope.get_waveform_samples(1, 'NORM'))
    outs = np.float32(scope.get_waveform_samples(2, 'NORM'))
    print(f'Got columns of sizes {len(ts)}, {len(ins)}, {len(outs)}')
    return ts, ins, outs

#----------------------------------------------------------------------
# MAIN PROGRAM RUNS A FREQUENCY SWEEP


print(f'{argv[0]} starting')

# Open connections to the hardware

scope = DS1054Z(scope_ip)
print('scope open')
fg = fygen.FYGen(fygen_port, debug_level=0)
print('fgen open')

# Set initial conditions on the oscilloscope
setup(scope, fg)

# Determine the frequencies at which to take data
freqs = np.logspace(np.log10(cmd_args.start_frequency),
                    np.log10(cmd_args.end_frequency),
                    num=cmd_args.frequency_steps)

Zmags = []                      # Accumulator for impedance magnitudes
phis = []                       # Accumulator for impedance phases
Rs = []                         # Accumulator for resistive components
Xs = []                         # Accumulator fo reactive components

# Run the frequency sweep
for f in freqs:
    print(f'get started, f={f}')
    ts, ins, outs = run_sweep(scope, fg, f)
    print('Ready to start analysis')
    Zmag, phi, R, X = analyze_sweep(f, ts, ins, outs)
    Zmags.append(Zmag); phis.append(phi), Rs.append(R), Xs.append(X)

# Save the collected data to a CSV file
csvFileName = cmd_args.runName[0] + '.csv'
with open(csvFileName, 'w', newline='') as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([
        'Freq', 'absZ', 'phi', 'R', 'X',
    ])
    csvWriter.writerows(zip(freqs, Zmags, phis, Rs, Xs))
    
# Plot the collected data for visual confirmation that the sweep worked
fig = plt.figure(figsize=(16, 9))
ax_zbar, ax_phi = fig.subplots(2, 1)

ax_zbar.plot(freqs, Zmags, label="Magnitude")
ax_zbar.plot(freqs, Rs, label="Resistance")
# ax_zbar.plot(freqs, abs(np.array(Xs, np.float)), label="Reactance")

ax_zbar.set_xscale('log')
ax_zbar.set_yscale('log')
ax_zbar.set_ylim(3, 50)

ax_zbar.grid(visible="true", which="major", axis="x")
ax_zbar.grid(visible="true", which="minor", axis="x")
ax_zbar.grid(visible="true", which="minor", axis="y")

Rticks = np.append(np.arange(6., 21., 2), np.array([20., 25., 30.]))
ax_zbar.yaxis.set_minor_locator(ticker.FixedLocator(Rticks))
ax_zbar.yaxis.set_major_locator(ticker.NullLocator())
ax_zbar.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax_zbar.yaxis.set_minor_formatter(ticker.ScalarFormatter())

ax_zbar.legend()

ax_zbar.set_title('Speaker impedance (ohms)')

ax_phi.plot(freqs, np.array(phis, dtype=float)*180/pi)

ax_phi.set_title('Phase angle of speaker impedance (degrees, +=inductive, -=capacitive)')

ax_phi.set_xscale('log')
ax_phi.grid(visible="true", which='major', axis='x')
ax_phi.grid(visible="true", which='minor', axis='x')
ax_phi.grid(visible="true", which='major', axis='y')


fig.tight_layout()
pngFileName = cmd_args.runName[0] + '.png'
print(f'Save to {pngFileName}')
plt.savefig(pngFileName, dpi=120)
plt.show()
