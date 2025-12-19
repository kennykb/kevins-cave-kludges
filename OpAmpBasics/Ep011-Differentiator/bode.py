import numpy as np
from numpy import abs, angle, log10, logspace, pi, sqrt, zeros
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

HzFormatter = EngFormatter(unit='Hz', places=1, sep='\N{THIN SPACE}')
dBFormatter = EngFormatter(unit='dB', places=1, sep='\N{THIN SPACE}')

def par(a, b):
    '''
    parallel impedances: return a||b
    '''
    return a*b/(a+b)

class Diff():
    '''
    Model of a differentiator
    '''
    def __init__(self, R1=1e3, C1=10e-9, R2=100e3, C2=100e-12):
        '''
        Parameters;
        R1 - input resistor
        C1 - input capacitor
        R2 = feedback resistor
        C2 - compensation capacitor
        '''

        self.R1 = R1
        self.C1 = C1
        self.R2 = R2
        self.C2 = C2

    def Zin(self, f):
        '''
        Return the impedance of the R1/C1 network

        Parameters:
        f - Frequency
        '''
        return self.R1 + 1j/(2*pi*f*self.C1)

    def Zfb(self, f):
        '''
        Return the impedance of the R2/C2 network

        Parameters:
        f - Frequency
        '''
        if self.C2 == 0:
            return self.R2
        else:
            return par(self.R2, 1j/(2*pi*f*self.C2))

    def Av(self, f):
        '''
        Return the idealized circuit gain as a complex number

        Parameters:
        f - Frequency
        '''
        return -self.Zfb(f)/self.Zin(f)

    def Gv(self, f):
        '''
        Return the modulus of the idealized circuit gain in decibels

        Parameters:
        f - Frequency
        '''
        return 20*log10(abs(self.Av(f)))

    def phi(self,f):
        '''
        Return the idealized circuit phase shift in degrees

        Parameters:
        f - Frequency
        '''
        alpha = -angle(self.Av(f), True)
        alpha = np.where(alpha < 0, alpha, alpha-360.0)
        return alpha

    def bode(self, ax, title='Bode plot'):
        '''
        Produce a Bode plot of the circuit

        Parameters:
        ax - matplotlib Axes object where the plot should be produced
        title = Title of the plot
        '''

        f1 = 1/(2*pi*self.C1*self.R2)
        fc = None
        f2 = None

        if self.R1 > 0 and self.C2 > 0:
            f2 = 1/(2*pi*self.R1*self.C2)
            fc = 1/(2*pi*sqrt(self.R1*self.C1*self.R2*self.C2))
            print(f'fc={fc}')
        elif self.R1 > 0:
            fc = 1/(2*pi*self.C1*self.R1)
        elif self.C2 > 0:
            fc = 1/(2*pi*self.R2*self.C2)

        fs = logspace(1, 7, num=70)

        Gs = self.Gv(fs)
        phis = self.phi(fs)
        minG = min(Gs)
        maxG = max(Gs)
        Grange = maxG - minG
        lowG = minG - 0.2*Grange
        highG = maxG + 0.05*Grange
        minphi = min(phis)
        maxphi = max(phis)
        phirange = maxphi-minphi

        ax.set_title(title)
        ax.set_xscale('log')
        ax.set_xlabel('Frequency (Hz)', color='k')
        ax.xaxis.set_major_formatter(HzFormatter)
        ax.set_ylabel('Gain (dB)', color='b')
        ax2 = ax.twinx()
        ax2.set_ylabel('Phase shift (deg)', color='r')
        ax2.set_ylim(minphi-0.15*phirange, maxphi + 0.05*phirange)
        ax2.set_yticks(np.arange(-90.0, minphi-7.5, -30.0))
        
        ax.plot(fs, zeros(fs.shape), '-k', linewidth=0.5)
        ax.plot([f1, f1], [lowG, highG], '-k', linewidth=0.5)
        if self.R1 > 0 and self.C2 > 0:
            ax.plot([f2, f2], [lowG, highG], '-k', linewidth=0.5)
        ax.annotate(HzFormatter(f1), xy=(f1*1.1, lowG),
                    horizontalalignment='left',
                    verticalalignment='bottom')
        if fc is not None:
            ax.plot([fc, fc], [lowG, highG], '-k', linewidth=0.5)
            ax.annotate(HzFormatter(fc), xy=(fc*1.1, lowG),
                        horizontalalignment='left',
                        verticalalignment='bottom')
        if f2 is not None:
            ax.annotate(HzFormatter(f2), xy=(f2*1.1, lowG),
                        horizontalalignment='left',
                        verticalalignment='bottom')
            
        # first asymptote
        if fc is None:
            fmax = 1e7
        else:
            fmax = 2*fc
        xs = np.array([10, fmax])
        ys = 20 * log10(xs / f1)
        ax.plot(xs, ys, '--b', linewidth=0.5)
        
        fmid = sqrt(10*fmax)
        Gmid = self.Gv(fmid)
        ax.annotate('6\N{THIN SPACE}dB/octave',
                    xy=(0.9*fmid, Gmid+0.1),
                    horizontalalignment='right',
                    verticalalignment='bottom',
                    color='b')

        # max gain
        if self.R1 > 0 and self.C2 <= 0:
            Gmax = 20 * log10(self.R2/self.R1)
            ax.plot([10, 1e7], [Gmax, Gmax], '--b', linewidth=0.5)
            ax.annotate(dBFormatter(Gmax), xy=(1e7, Gmax+1),
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        color='b')
        elif self.R1 <= 0 and self.C2 > 0:
            Gmax = 20 * log10(self.C1/self.C2)
            ax.plot([10, 1e7], [Gmax, Gmax], '--b', linewidth=0.5)
            ax.annotate(dBFormatter(Gmax), xy=(1e7, Gmax+1),
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        color='b')
        elif self.R1 > 0 and self.C2 > 0:
            Gmax = self.Gv(fc)
            ax.annotate(dBFormatter(Gmax), xy=(10, Gmax+1),
                        horizontalalignment='left',
                        verticalalignment='bottom',
                        color='b')
            ax.plot([10, fc], [Gmax, Gmax], ':b', linewidth=0.5)

        # second asymptote

        if f2 is not None:
            fmin = 0.5 * fc
            xs = np.array([fmin, 1e7])
            ys = 20*log10(f2/xs)
            ax.plot(xs, ys, '--b', linewidth=0.5)
            fmid = sqrt(fc*1e7)
            Gmid = self.Gv(fmid)
            ax.annotate('-6\N{THIN SPACE}dB/octave',
                        xy=(1.1*fmid, Gmid+0.1),
                        horizontalalignment='left',
                        verticalalignment='bottom',
                        color='b')
            
            
        ax.plot(fs, Gs, '-b')
        ax2.plot(fs, phis, '-r')


ckt1 = Diff(R1=0, C2=0)
fig = plt.figure(figsize=(8, 4.5), dpi=200)
ax = fig.add_subplot(1, 1, 1)
ckt1.bode(ax, title="'Ideal' differentiator")
fig.savefig('Images/diff-ideal.png', dpi=200)

ckt2 = Diff(R1=1000, C2=0)
fig = plt.figure(figsize=(8, 4.5), dpi=200)
ax = fig.add_subplot(1, 1, 1)
ckt2.bode(ax, title="Differentiator with input resistor added")
fig.savefig('Images/diff-with-R1.png', dpi=200)

ckt3 = Diff(R1=1000, C2=100e-12)
fig = plt.figure(figsize=(8, 4.5), dpi=200)
ax = fig.add_subplot(1, 1, 1)
ckt3.bode(ax, title="Practical differentiator")
fig.savefig('Images/diff-integ.png', dpi=200)

plt.show()

