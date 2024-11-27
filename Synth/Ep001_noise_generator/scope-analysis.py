import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import periodogram, welch
from scipy.stats import norm
import sys

# argv[1] is the name of the CSV file saved off the oscilloscope

samplefile = sys.argv[1]

# liszt - list of observed values, in time order
# startval - initial time point
# incrval - time increment

liszt = []
with open(samplefile, newline='') as csvfile:
    rdr = csv.reader(csvfile)
    n = 0
    for row in rdr:
        n = n + 1
        if n == 2:
            startval = float(row[2])
            incrval = float(row[3])
            print(f'Start={startval} Incr={incrval}')
        elif n >= 3:
            val = np.float32(row[1])
            liszt.append(val)
print(f'N = {len(liszt)}')
liszt = np.array(liszt, dtype=np.float32)

# uniq - unique observed values
# counts - counts of the observed values
# binwidth - width of bins using scope's quantization

uniq, counts = np.unique(liszt, return_counts=True)
binwidth = 1e38
for idx, val in enumerate(uniq):
    if idx > 0:
        thisbin = val - lastval
        if thisbin < binwidth:
            binwidth = thisbin
    lastval = val

# xbar - Sample mean
# sigma - Sample standard deviation
# gausscdf - Gaussian CDF corresponding to 'uniq' values
# empcdf - Empirical CDF corresponding to 'uniq' values

xbar = np.mean(liszt)
print(f'Mean value = {xbar}')
sigma = np.std(liszt)
gausscdf = norm.cdf((uniq  - xbar) / sigma)
empcdf = np.cumsum(counts) / liszt.shape[0]

fig = plt.figure(frameon=False, figsize=(16.0, 9.0))

# Figure 1 - Histogram of values (unequanl bins)

plt.title(f'Histogram of voltages\nMean = {xbar:.6f} Standard deviation = {sigma:.6f}')
plt.ylabel("Number of samples")
plt.xlabel("Voltage")
plt.hist(liszt, bins=uniq)

# Figure 2 - CDF

fig = plt.figure(frameon=False, figsize=(16.0, 9.0))

plt.title('Cumulative probability density of voltages')
plt.xlabel('Voltage')
plt.ylabel('Probability')
plt.step(uniq, empcdf, label='Observed', where='post')
plt.plot(uniq, gausscdf, 'k--', label='Gaussian')
plt.legend()

# Figrue 3 - CDF compared with Gaussian

fig = plt.figure(frameon=False, figsize=(16.0, 9.0))

plt.title('Probability density of voltages, compared with Gaussian')
plt.xlabel('Expected CDF for Gaussian distribution')
plt.ylabel('Empirical CDF for voltage samples')
plt.plot(gausscdf, empcdf)
plt.plot([0, 1], [0, 1])
plt.axis('square')

# Figure 4 - Power spectral densityu

fig = plt.figure(frameon=False, figsize=(16.0, 9.0))


freqs1, Pxx = welch(liszt,
                    fs=1.0/incrval,
                    window='hann',
                    nperseg = 0.05 / incrval)
plt.title('Spectrogram of noise')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power spectral density (V²/Hz)')
plt.semilogy(freqs1,Pxx)
plt.ylim([1e-8, 1e-6])

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9,
                    wspace=0.3, hspace=0.3)

plt.show()

