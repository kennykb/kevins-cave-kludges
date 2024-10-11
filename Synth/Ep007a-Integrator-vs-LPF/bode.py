#!/usr/bin/env python
"""
Produce a Bode plot of a device under test

Copyright 2024 by Kevin B. Kenny
Please refer to the 'LICENSE.txt' file in the software distribution for
the terms and conditions of reuse, and a DISCLAIMER OF ALL WARRANTIES.


Setup:

FY6900 signal generator and scope channel 1 should be connected to the
input of a device under test.

Scope channel 2 should be connected to the output.

The scope's vertical and horizontal scales will be set automatically
according to the test conditions.
"""

# Some of this stuff probably should be command line arguments,
# but I'm in a hurry.

import argparse
import csv
from ds1054z import DS1054Z
from fygen import fygen
from math import floor, pi
import matplotlib as mpl
from matplotlib import pyplot as plt
from time import sleep
from math import floor, log, log10
import numpy as np
import sys

parser = argparse.ArgumentParser\
    (description='Measure a filter and produce a Bode plot.')
parser.add_argument('csvFile', metavar='fileName.csv',
                    type=argparse.FileType('w'),
                    nargs=1,
                    help='CSV file that receives the plot data')
parser.add_argument('--start', dest='start_frequency',
                    type=float, default=20.0,
                    help='Starting frequency')
parser.add_argument('--end', dest='end_frequency',
                    type=float, default=20000.0,
                    help='Ending frequency')
parser.add_argument('--steps', dest='frequency_steps',
                    type=int, default=76,
                    help='Number of frequency steps to take')
cmd_args = parser.parse_args()
print(cmd_args)

# IP address of DS1054Z scope.
scope_ip = '192.168.2.101'

# USB-serial port communicating with FY6900 function generator
fygen_port = 'COM3'

# Frequency range to plot

start_frequency = cmd_args.start_frequency
end_frequency = cmd_args.end_frequency

# Amplitude of the wave to apply to the device under test

input_amplitude = 5

# Maximum output amplitude expected - usually should be a
# little bit bigger than the supply span

output_amplitude = 40

# Remember scope scales so that we can skip resetting if they don't change

scope_v_scales = [None, None, None, None]


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
    pass    

def lowlevel_set_ch1_freq(fg, freq):
    """
    the FYGen package sends the frequency without a decimal point.
    The FY6900 appears to expect that it will have a decimal point.
    Try to work around this.
    """
    # print(f'Set channel 1 frequency to {freq}')
    fg.send(f'WMF{freq:015.6f}')
    # print(f'Readback the frequency')
    # print(f'{fg.send("RMF")}')


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

    # print(f'For a vertical range of {mn} .. {mx} V, choose {retval} V/div')
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

    # print(f'At a frequency of {freq}, set scope timebase to {scale} s/div')
    # print(f'   and offset of {offset} s')

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
           volts=5,
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
    # print(f"Set frequency of {freq} Hz")
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

    Returns a pair (dB, phase) where db is the gain/loss of the circuit
    in decibels and phase is the phase lead/lag, suitable for adding to
    the Bode plot.
    """
    N = ts.shape[0] # Number of data ppoints

    time_per_step = (ts[-1] - ts[0]) / (N - 1) # Seconds per time step

    # Find the correlation between an ideal wave of the given
    # frequency and the observed data
    window = np.blackman(N)
    wave = np.sin(ts*(2*pi*freq))
    wwave = wave*window
    c_in = np.correlate(wwave, window*ins, "same")
    c_out = np.correlate(wwave, window*outs, "same")

    # The locations of the two peaks in the correlation give the
    # phase delay
    in_idx = fine_argmax(c_in)
    out_idx = fine_argmax(c_out)
    time_delay = time_per_step * (out_idx - in_idx)
    phase_delay_deg = time_delay * freq * 360
    while phase_delay_deg > 180:
        phase_delay_deg -= 360
    while phase_delay_deg < -180:
        phase_delay_deg += 360

    # Isolate the values for a complete number of cycles
    steps_per_cycle = 1/(freq * time_per_step)
    steps_to_sample = int(0.5 +
                          steps_per_cycle * (ts.shape[0] // steps_per_cycle))

    # Find the RMS voltage of the isolated values, removing any
    # DC component
    in_rms = np.std(ins[0:steps_to_sample])
    out_rms = np.std(outs[0:steps_to_sample])

    # Find the gain/loss in decibels
    dB = 20 * np.log10(out_rms / in_rms)

    # Return gain/loss and phase lead/lag
    return dB, phase_delay_deg

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

    setup_one_freq(scope, fg, freq)
    scope.run()
    sleep(10.0/freq + 0.25)
    scope.stop()
    ts = np.float32(scope.waveform_time_values)
    ins = np.float32(scope.get_waveform_samples(1, 'NORM'))
    outs = np.float32(scope.get_waveform_samples(2, 'NORM'))
    return ts, ins, outs

print('bode.py starting')

scope = DS1054Z(scope_ip)
fg = fygen.FYGen(fygen_port, debug_level=0)

setup(scope, fg)

writer = csv.DictWriter(cmd_args.csvFile[0],
                        fieldnames=['Freq', 'Gain', 'Phase'])

writer.writeheader()
freqs = np.logspace(np.log10(cmd_args.start_frequency),
                    np.log10(cmd_args.end_frequency),
                    num=cmd_args.frequency_steps)
gs = []
phs = []
for f in freqs:
    print(f'get started, f={f}')
    ts, ins, outs = run_sweep(scope, fg, f)
    g, ph = analyze_sweep(f, ts, ins, outs)
    gs.append(g)
    phs.append(ph)
    writer.writerow({'Freq': f, 'Gain': g, 'Phase': ph})

del writer
del cmd_args.csvFile

fig, ax1 = plt.subplots()
ax1.set_xlabel('Frequency (Hz)')
ax1.set_xscale('log')
ax1.set_ylabel('Gain (dB)', color='tab:blue')
ax1.plot(freqs, gs, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue', color='tab:blue')
ax2 = ax1.twinx()
ax2.set_ylabel('Phase (degrees)', color='tab:red')
ax2.plot(freqs, phs, color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red', color='tab:red')
fig.tight_layout()
plt.show()

