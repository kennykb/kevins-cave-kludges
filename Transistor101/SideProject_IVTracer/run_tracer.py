#!/usr/bin/env python
"""
run_tracer.py --

Collects transitor current-vs-base-voltage curve.

Cppyright (c) 2024 by Kevin B. Kenny.
Please refer to the 'LICENSE.txt' file in the software distribution for
the terms and conditions of reuse, and a DISCLAIMER OF ALL WARRANTIES.

Usage:  run_tracer.py <deviceName>

Arguments:
    deviceName - Name of a device, to be substituted into the name of
                 data files produced by the run.

Results:
    Produces a file, 'deviceName.csv' containing voltage and current samples.

This program presumes a Rigol 1000Z -series oscilloscope is connected
to a test rig whose schematic appears as 'tracer-revF/ elsewhere in this
project.

The initial settings for the scope should be that channel 1 is connected
to the base voltage readout (U1, pin 7) and channel 2 is connected to
the emitter current readout (U1, pin 8). THe scope should be set
to read out dual trace voltage-vs-time on channels 1 and 2, and to trigger
on the falling edge of the channel 2 signal at roughtly the midpoint
of its range. Channel 2 should be set to 2V/division, with an offset of -8V.

The program prompts the operator to change the transresistance setting
of the current sense amplifier in the test rig, and for each setting,
collects a set of voltage-vs-current curves.  It plots the individual
samples as a 2-d histogram, and fits a line through the observed data
(on a semi-log scale, so that the actual fitted function is exponential).
It produces a CSV file containing the collrected samples, in case further
analysis is required.
"""

# REQUIRED EXTERNAL MODULES
#    All required modules are present on PyPI at the time of writing of this
#    program.

import csv
from ds1054z import DS1054Z
import matplotlib as mpl
from matplotlib import pyplot as plt
from time import sleep
from math import floor, log, log10
import numpy as np
import sys

# IP address of the scope.
scope_ip = '192.168.2.101'

# Number of sweeps to take at each transresistance setting.
replicates = 16

# Voltage readout gain
#    As seen in the build video, a decision was made late in the build
#    process to decrease the gain of the voltage readout from 10 to 5,
#    in order to show the curve for a typical red LED.
# v_readout_gain = 10 # Earlier version
v_readout_gain = 5 # Current version

def stop_scope(scope):
    '''
    Stops the oscilloscope and makes sure that (a) it has had time to stop,
    (b) it actually acted on the 'stop' command.
    '''
    scope.stop()
    while scope.query(':TRIG:STAT?') != 'STOP':
        sleep(0.1)
        scope.stop()

def set_safe_ranges(scope):
    '''
    Sets the scope timebase and channel 1 scale wide enough to accommodate
    the expected ranges in the voltage and current readouts.

    Arguments:
        scope - Handle to the oscilloscope

    The expected voltage range is 0..10 V,
    and 2 ms/div is considered a 'safe' timebase scale.
    '''
    stop_scope(scope)
    scope.set_channel_scale(1, 2.000)
    scope.set_channel_offset(1, -8.000)
    scope.set_channel_scale(2, 2.0)
    scope.set_channel_offset(2, -8.0)
    scope.timebase_scale=0.002
    scope.timebase_offset = 5*0.002

class ScopeFault(Exception):
    pass
    
def sweep(scope, ch=1):
    '''
    Arguments:
        scope - Handle to the oscilloscppe
        ch - Channel that must have data at the end of the sweep

    Results:
        Returns the range of values collected in the given channel
    
    Stops the oscilloscope, waits for it to stop,
    then runs it for a short period of time and stops it again,
    to collect at least one screen of waveform data.

    Ideally, this logic would set the scope's trigger mode to
    SNGL (single trigger) and collect a single sweep. I've not managed
    to make that work in testing; every sequence I've tried collects
    a partial sweep, displays 'Input invalid!' on the scope screen,
    and throws an assertion failure when trying to read the wavefform.
    '''
    stop_scope(scope)
    scope.run();
    sleep(0.25)
    stop_scope(scope)
    # Stray inductance on the breadboard might cause out-of-range
    # measurements, which causes the 'scope to readout None for
    # Vmin or Vmax
    vmin = scope.get_channel_measurement(ch, 'vmin')
    vmax = scope.get_channel_measurement(ch, 'vmax')
    if vmin is None or vmax is None:
        meas = scope.get_waveform_samples(ch, 'NORM')
        vmin = 100
        vmax = -100
        for v in meas:
            if v is not None:
                if v < vmin:
                    vmin = v
                if v > vmax:
                    vmax = v
        if vmin < vmax:
            print('Could not read out any voltages from scope')
            raise ScopeFault()
    return vmin, vmax

def autoscale_vertical(scope, ch):
    '''
    Adjusts the vertical scale for one of the scope channels.

    Arguments:
        scope - Handle to the oscilloscope
        ch - Channel number to adjust.

    This procedure assumes that the channel has been preset to a range
    wide enough that the waveform will not overflow the readout range
    at either end.  It runs the scope for a short period of time,
    then queries the channel for the observed voltage rage.

    It pads the range by 5% for safety, and finds a suitable step size
    and vertical offset to make the trace as large as possible on the
    readout (and hence, give the readout the greatest possible precision).

    It sets scale and offset accordingly.
    '''

    # Reset the scope to wide ranges
    set_safe_ranges(scope)

    # Get observed voltage range
    vmin, vmax = sweep(scope, ch)
    
    # Pad out the range a little for safety
    rng = (vmax - vmin)
    vmin -= 0.05 * rng
    vmax += 0.05 * rng

    # Find a suitable step size
    step = (vmax - vmin) / 8
    decade = 10**floor(log10(step))
    for u in [1, 2, 5, 10, 20]:
        newstep = u*decade
        bottom = newstep*floor(vmin / newstep)
        top = bottom + 8*newstep
        if (top >= vmax):
            break

    # Set the new step size and compute a vertical offset
    scope.set_channel_scale(ch, newstep)
    scope.set_channel_offset(ch, -bottom-4*newstep)

def autoscale_timebase(scope):
    '''
    Sets the timebase scale and offset once the vertical scale
    is established.

    Arguments:
        scope - Handle to the oscilloscope
    '''

    # Collect one waveform for horizontal analysis
    sweep(scope)
    vs = scope.get_waveform_samples(1, 'NORM')
    ts = scope.waveform_time_values
    vmin = np.min(vs)
    vmax = np.max(vs)

    # Set trigger labels based on the voltage range
    
    utrigpt = 0.25*vmin + 0.75*vmax # Upper trigger - 75% of range
    ltrigpt = 0.75*vmin + 0.25*vmax # Lower trivver - 25% of range

    # Follow the voltage trace from channel 1 and find the first
    # two falling edges.
    state = 'idle'
    for t, v in zip(ts, vs):
        t = float(t)
        v = float(v)
        if state=='idle' and v >= utrigpt:
            state='high1'
        elif state=='high1' and v <= ltrigpt:
            ltrig1 = t
            state='low1'
        elif state=='low1' and v >= utrigpt:
            state = 'high2'
        elif state=='high2' and v <= ltrigpt:
            ltrig2 = t
            break

    # Calculate duration between the two falling edges,
    # and set the scope timebase to fit the duration on the screen
    dur = ltrig2-ltrig1
    step = 10**(floor(log10(dur)))
    for d in [100, 50, 20, 10, 5, 2, 1]:
        if 12*step/d > dur:
            step = step/d
            break
    scope.timebase_scale=step
    scope.timebase_offset=6*step

def collect_1sweep(scope, vscale, iscale):
    '''
    Collects the data for one replicate in one set of test conditions.

    Arguments:
        scope - Handle to the oscilloscope
        vscale - Scale factor for base voltages (unitless).
        iscale - Scale factor for emitter currents (volts per mA).

    This is the procedure that collects the rising portion of the
    current waveform.  It collects one sweep worth of waveform samples,
    isolates the rising portion, and returns it as two lists, 'vs' and 'is'.

    The rising portion is identified by
    (1) Waiting for the current readout to drop below 2% of full scale.
    (2) Waiting for the current readout to rise again above 4%.
    (3) Accumulating samples until the current readout is at full scale.

    The samples are scaled by 'vscale' (the voltage gain of the voltage
    readout) and 'iscale' (the gain of the current readout,
    mA per volt).

    Full scale is assumed to be 10 volts on the scale of the current readout.
    '''
    vs_return = []
    is_return = []
    while (len(vs_return) == 0):
        sweep(scope)
        vs = scope.get_waveform_samples(1, 'NORM')
        iis = scope.get_waveform_samples(2, 'NORM')
        state = 'idle'
        for rawv, i in zip(vs, iis):
            v = rawv/vscale
            if state == 'idle' and i <= 0.2:
                state = 'waiting'
            elif state == 'waiting' and i >= 0.4:
                state = 'collecting'
            elif state == 'collecting' and i >= 9.0 :
                lasti = i
                state = 'terminating'
            elif state == 'terminating' and i < lasti-0.2:
                break
            if state == 'collecting' or state == 'terminating':
                vs_return.append(v)
                is_return.append(i*iscale)
    return vs_return, is_return

def run1scale(scope, vscale, iscale, replicates):
    '''
    Collects data for one scale of readout (1 V = {iscale} mA)

    Arguments:
        scope - Handle to the oscilloscope
        vscale - Voltage scale (unitless)
        iscale - Current scale (1 V = {iscale} mA)
        replicates - Number of replicates to collect

    Results:
        Returns a pair of lists: one of raw voltage measurements,
        and the second of raw current meeasurements correspoiding
        to the voltages.
    '''

    # Prompt the operator
    # The Enter kkkkey on my kkkeboard sometimes stttutttters.
    while input(f'''Set scale to 1V = {iscale} mA and say 'ok': ''') != 'ok':
        pass

    # Scale the scope axes
    autoscale_vertical(scope, 1)
    autoscale_timebase(scope)

    # Collect voltage and current data, filtering out samples where the
    # current is less than either 8% of full scale or 100 nA.
    rawv = []
    rawi = []
    for n in range(0, replicates):
        print(f'collecting sweep #{n} of {replicates}')
        vs, iis = collect_1sweep(scope, vscale, iscale)
        for (v, i) in zip(vs, iis):
            if i < 0.8 * iscale or i <= 0:
                continue
            rawv.append(v)
            rawi.append(i)
    return rawv, rawi

def analyze_results(rawvs, rawis):
    '''
    Analyzes the results of the run.

    Arguments;
        rawvs - Readings of the voltages during all the sweeps
        rawis - Readings of the currents during all the sweeps

    This procedure produces a 2-d histogram of all the voltage
    and current observations, on a semi-log scale.

    It then fits a line to the plotted observations, displays that line on
    the plot, and overlays the plot with the equation of the line.
    It returns the calculated saturation current and exponential scale
    as a pair of floating point numbers.
    '''

    # Coerce the voltages and currents to NumPy arrays
    rawvs = np.array(rawvs, dtype=np.float32)
    rawis = np.array(rawis, dtype=np.float32)

    # Calculate voltage and current ranges
    minv = np.min(rawvs); maxv = np.max(rawvs)
    mini = np.min(rawis); maxi = np.max(rawis)
    logmini = np.log(mini); logmaxi = np.log(maxi)
    print(f'I in ([{mini} : {maxi}])')

    # Calculate data ranges for semi-log plot
    v_space = np.linspace(minv, maxv, 128)
    i_space = np.logspace(np.floor(np.log10(mini)) - 0.5,
                          np.ceil(np.log10(maxi)) + 0.5, 128)

    # Plot the histogram

    plt.figure(1, figsize=(8, 4.5), dpi=240)
    plt.tight_layout()
    plt.title(title)
    plt.hist2d(rawvs, rawis,
               bins=(v_space, i_space),
               norm=mpl.colors.LogNorm(),
               cmap='cividis')
    plt.yscale("log")
    plt.xlabel('Drive voltage (V)')
    plt.ylabel('Output current (mA)')

    # Fit a line to the observed data
    rawlogis = np.log(rawis)
    p = np.polyfit(rawvs, rawlogis, 1)

    # Plot the fitted line
    vsm = np.linspace(minv, maxv, 128)
    ism = np.exp(p[0]*vsm + p[1])
    plt.plot(vsm, ism, 'k--', lw=1.5)

    # Convert fit parameters to Is and eta*Vt
    Is = np.exp(p[1])
    oneover_eta_Vt = 3*np.log(10)+p[0]
    eta_Vt = 1 / oneover_eta_Vt
    m = f'I = {Is:e} * exp(V / {eta_Vt:e})'

    # Overlay fitted function onto the display
    tx = 0.95 * minv + 0.05 * maxv
    ty = np.exp(0.85 * logmaxi + 0.15 * logmini)
    plt.text(tx, ty, m, fontsize='small', color='black')

    # If this is a transistor, also plot the curve assuming Vt=0.025
    if title[-1] == 'V':
        meanlogi = np.mean(rawlogis)
        meanvovt = np.mean(rawvs) / 0.025
        logIs2 = meanlogi - meanvovt
        Is2_mA = np.exp(logIs2)
        ism = Is2_mA  * np.exp(vsm / 0.025)
        plt.plot(vsm, ism, 'b--', lw=1.5)
        m = f'I = {0.001*Is2_mA:e} * exp(V/0.025)'
        tx = 0.95 * minv + 0.05 * maxv
        ty = np.exp(0.8 * logmaxi + 0.2 * logmini)
        plt.text(tx, ty, m, fontsize='small', color='blue')
    
    return Is, eta_Vt
        

def save_results(title, rawvs, rawis):
    """
    Saves the results of a run into a CSV file

    Arguments:
        title - Name of the CSV file.  '.cev' will be appended to the name
        rawvs - Voltage samples
        rawis - Current samples
    """

    with open(f'{title}-ivcurve.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['V', 'I'])
        for V, I in zip(rawvs, rawis):
            csvwriter.writerow([V, I])

# MAIN PROGRAM

# Title of the run, usually the device name
title = sys.argv[1]

# Initialization: Open the scope, and set the current readout scale
# to span (0..10) V.

scope = DS1054Z(scope_ip)

# Collect all the raw data

rawvs = []
rawis = []
for scale in [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0]:
    rawv, rawi = run1scale(scope, v_readout_gain, scale, replicates)
    rawvs.extend(rawv)
    rawis.extend(rawi)

# Analzye the data and print a one-line summary
Is, eta_Vt = analyze_results(rawvs, rawis)
print(f'{title}: I = {Is} * exp(V / {eta_Vt:e})')

# Save the results to a file

save_results(title, rawis, rawvs)

plt.show();

