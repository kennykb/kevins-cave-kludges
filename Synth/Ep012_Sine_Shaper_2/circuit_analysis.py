import inspect
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np
import scipy
import sympy

#-----------------------------------------------------------------------------
#
# Problem definition
#
#-----------------------------------------------------------------------------

# Maximum output voltage
Vout_max = 3

# Maximum input voltage
Vin_max = Vout_max * np.pi/2

# Number of diodes in each side of the ladder
ndiodes = 6

def f(x, A):
    '''
    The function being approximated: A*sin(x/A)
    '''
    return A*sympy.sin(x/A)

# Make Python code to evaluate the function numerically.
#-The above definitions are symbolic.
x = sympy.symbols('x')
A = sympy.symbols('A', positive=True)
feval = sympy.lambdify([x, A], f(x, A), modules=['scipy', 'numpy'])
print('FYI: Python code for function:')
print(inspect.getsource(feval))

print('----------------------------------------------------------------------')

def pwl(y0, m, h):
    '''
    Computes a value in one segment of the piecewise linear approximation.
    The abscissa is x0+h, the slope is m, and the ordinate of the left-hand
    end of the segmant is y0.
    '''
    return y0 + m*h

def pwlerror(x0, y0, m, h, A):
    '''
    Computes the error at the abscissa x0+h in the piece of the approximation
    that starts at (x0, y0) and has a slope of m
    '''
    return f(x0+h, A) - pwl(y0, m, h)

def pwlerror2(x0, y0, m, h, A):
    '''
    Computes the squared error at the abscissa x0+h in the piece of the
    approximation that starts at (x0, y0) and has a slope of m
    '''
    return pwlerror(x0, y0, m, h, A)**2

def intpwlerror2(x0, w, y0, m, A):
    '''
    Computes the integral of the squared error across the interval that
    starts at (x0, y0), has a slope of m and a width of w.
    '''
    h = sympy.symbols('h')
    return sympy.integrate(pwlerror2(x0, y0, m, h, A), (h, 0, w))

# Function to evaluate the error over one interval numerically
x0, w, y0, m = sympy.symbols('x0 w y0 m')
A = sympy.symbols('A', positive=True)
pwl_error_on_interval = sympy.lambdify(
    [x0, w, y0, m, A],
    sympy.expand_trig(intpwlerror2(x0, w, y0, m, A)),
    modules=['scipy', 'numpy'],
    cse=True,
)

print('FYI: Formula for the integrated squared error in one interval:')
print(intpwlerror2(x0, w, y0, m, A).simplify())
print('FYI: Integral reduced to Python code:')
print(inspect.getsource(pwl_error_on_interval))
print('')
print('----------------------------------------------------------------------')

A = Vout_max

def objective(params, argvec):
    '''
    Calculates the integral of the squared error of the piecewise
    linear function across its entire domain [0 .. Vin_max]

    The parameter vector 'params' consists of 'ndiodes' interval widths,
    followed by 'ndiodes-1' or 'ndiodes' slopes.
    There are actually 'ndiodes+1' intervals. The final interval has
    a width of 'Vin_max' minus the sum of the other interval widths.
    If the length of the parameter vector is odd, then the slope of the
    approximation is zero in the final interval.

    argvec[0] is the value of Vin_max, the maximum input voltage
    argvec[1] is the value of A, the maxiumum output voltage
    '''
    Vin_max = argvec[0]
    A = argvec[1]

    # Number of intervals
    n = (len(params)+1)//2

    # Widths of the intervals
    ws = params[0:n]
    ws = np.concatenate([ws, [Vin_max-sum(ws)]])

    # Slopes in the intervals
    ms = np.concatenate([[1], params[n:]])
    if len(ms) < len(ws):
        ms = np.concatenate([ms, [0]])

    # Starting and ending points of the intervals
    x1s = np.cumsum(ws)
    x0s = np.concatenate([[0], x1s[:-1]])

    # Starting y's for the intervals
    y0s = np.concatenate([[0], np.cumsum(ws*ms)[:-1]])

    # Integrated square errors over all the intervals
    errors = pwl_error_on_interval(x0s, ws, y0s, ms, A)

    # Sum up the integrals for all the intervals and return the
    # integrated squared error.
    return sum(errors)


#-----------------------------------------------------------------------------
#
# Functions needed for the optimization process that selects the breakpoints
#
#-----------------------------------------------------------------------------

def initial_guess(Vin_max, Vout_max, ndiodes):
    '''
    Develops the initial guess for the optimization parameters.

    We simply place 'ndiodes+2' equally spaced points, including the
    ends of the interval.
    '''

    xs = np.linspace(0, Vin_max, ndiodes+2)
    ys = feval(xs, Vout_max)

    # Widths of the intervals
    ws = xs[1:]-xs[:-1]
    
    # Slopes of the segments
    ms = (ys[1:]-ys[:-1])/ws
    
    # Repack the widths and slopes into the parameter array
    return np.concatenate([ws[:-1], ms[1:]])

def param_bounds(Vin_max, ndiodes):
    '''
    Sets bounds on the model variables. The interval widths must
    nonnegative. The slopes must be in the range [0 .. 1].
    '''
    
    return np.array([(0, np.inf)]*ndiodes + [(0, 1)]*(ndiodes))

def param_constraints(ndiodes):
    '''
    Sets constraints on the model variables.  The sum of the interval
    widths must be at most Vin_max, and the slopes must decrease
    monotonically.
    '''

    # Construct the remaining constraints
    constraint_mtx = []
    lb = []
    ub = []

    # The sum of the interval widths may not exceed Vin_max
    constraint_mtx.append([1]*ndiodes + [0]*(ndiodes))
    lb.append(-np.inf)
    ub.append(Vin_max)
    print('constraint row 0')
    print(constraint_mtx[0])

    # The slopes of the segments must decrease monotonically
    for i in range(0, ndiodes-1):
        row = [0]*(ndiodes+i) + [1, -1] + [0]*(ndiodes-2-i)
        print(f'constraint row {i+1}')
        print(row)
        constraint_mtx.append(row)
        lb.append(0)
        ub.append(np.inf)

    # Package the constraints
    return scipy.optimize.LinearConstraint(constraint_mtx, lb, ub)

#-----------------------------------------------------------------------------
#
# Class that represents a partly-constructed diode ladded.
#
#----------------------------------------------------------------------

class Ladder:

    def __init__(self, Vmax=3, Imax=0.005, Vmax_in=None,
                 Vref=None, Iref=None, Rin=None, Rtail=None,
                 Vdiode=0.55, Rdiode=33):
        '''
        Makes an empty diode ladder.

        Vmax_in - Maxiumu input voltage that's expected
        Vmax - Output voltage when Vin=Vmax_in, defau
        Imax - Maximum input current that's allowed
        Vref - Reference voltage
        Iref - Maximum current provided by the reference source
        Vdiode - Forward voltage drop of a diode
        Rdiode - Resistance of diode
        '''

        # Maximum output voltage
        self.Vmax_out = Vmax
        # Maximum inpur current
        self.Imax_in = Imax
        # Maximum input voltage
        if Vmax_in is None:
            Vmax_in = self.Vmax_out*np.pi/2
        self.Vmax_in = Vmax_in
        # Reference voltage
        if Vref is None:
            Vref = Vmax - Vdiode
        self.Vref = Vref
        # Maximum reference current
        if Iref is None:
            Iref = 1.05 * self.Imax_in
        self.Imax_ref = Iref
        # Input resistor
        if Rin is None:
            Rin = (self.Vmax_in - self.Vmax_out) / self.Imax_in
        self.Rin = Rin
        if Rtail is None:
            Rtail = self.Vref / self.Imax_ref
        self.Rtail = Rtail
        # Diode forward drop
        self.Vdiode = Vdiode
        # Diode resistance
        self.Rdiode = Rdiode

        # Equivelent wye circut to the ladder so far

        # Resistor to ground
        self.Rx = 0
        # Resistor to the output voltage
        self.Ry = 1e12
        # Resistor to the referencce voltage (Rtail will be added)
        self.Rz = 0

        # Voltages at the nodes as of the last change to this object
        self.Vin_last = 0
        self.Vout_last = 0
        self.Vz_last = 0

        # Rate of change of Vout wrt Vin
        self.m = 1
        # Rate of change of Vz wrt Vin
        self.k = 0


    def analysis_find_breakpoint(self, Ra):
        '''
        # Given the lower resistor, finds the input voltage, lower voltage,
        # and output voltage at the next breakpoint, and updates them
        # in this object
        #
        # Ra - lower resistor
        #
        # Result: None
        #
        # Side effects:
        #     Updates the breakpoint voltages.
        '''

        # Find the distance to the next breakpoint
        deltaVin = (Ra*(self.Vref - self.Vz_last) \
                    + self.Rtail*(self.Vdiode - self.Vout_last + self.Vz_last)) \
                    /(Ra*self.k - self.Rtail*self.k + self.Rtail*self.m)
        deltaVout = self.m * deltaVin
        self.Vin_last, self.Vz_last, self.Vout_last = \
            self.Vin_last + deltaVin, \
            self.Vout_last + deltaVout - self.Vdiode, \
            self.Vout_last + deltaVout

        
    def analysis_find_equivalents(self, Ra, Rb):
        '''
        Given the lower and upper resistors, Ra and Rb respectively,
        finds the wye-circuit equivalent of the current network with
        the next diode conducting.

        Side effects:
        Updates Rx, the resistor to constant voltage, Ry, the resistor
        to the output, and Rz, the resistor to the voltage divider.
        '''

        D = Ra + Rb + self.Rdiode + self.Ry + self.Rz
        self.Rx, self.Ry, self.Rz, self.Rtail = \
            self.Rx + self.Ry*(Ra + self.Rz) / D, \
            self.Ry*(Rb + self.Rdiode) / D, \
            (Ra + self.Rz)*(Rb + self.Rdiode)/ D, \
            self.Rtail - Ra

        
    def analysis_find_slopes(self):
        '''
        Updates m, the output rate of change wrt the input voltage,
        and k, the rate of change of the lower divider voltage wrt
        the input voltage,
        '''

        R1 = self.Rz + self.Rtail
        R2 = self.Rx*R1/(self.Rx + R1)
        R3 = R2 + self.Ry
        R4 = R3 + self.Rin
        self.m = R3 / R4
        self.k = (R2 / R4)*(self.Rtail/R1)

            
    def analysis_add_stage(self, Ra, Rb):
        '''
        Adds one stage (two resistors and a diode) to a circuit analysis.
        Ra - lower series resistor, part of the divider stack
        Rb - upper shunt resistor (with a diode in series)
        '''
        self.analysis_find_breakpoint(Ra)
        self.analysis_find_equivalents(Ra, Rb)
        self.analysis_find_slopes()
        

    def synthesis_find_Ra(self, Vin_next):
        '''
        Finds a resistor that will give the appropriate divider
        voltage to make the diode start conducting at the given
        input voltage
        '''
        deltaVin = Vin_next - self.Vin_last
        Vout_now = self.m*deltaVin + self.Vout_last
        Vz_now = self.k*deltaVin + self.Vz_last
        Ra = self.Rtail*(Vout_now - Vz_now - self.Vdiode)/(self.Vref - Vz_now)
        return Ra

    def synthesis_find_Rb(self, Ra, m_next):
        '''
        Finds the next shunt resistor, given the next slope and the value
        of the lower series resistor
        '''

        # What is the equivalent resistance of the bridge?
        Rlower = self.Rin*m_next/(1-m_next)

        # Convert the lower delta of the bridge to a wye
        Rc = self.Rz + Ra
        Rd = self.Rtail - Ra
        D = self.Rz + self.Rtail + self.Rx
        Rp = self.Rx*Rc/D
        Rq = self.Rx*Rd/D
        Rr = Rc*Rd/D

        # Solve the bridge for Rb
        Rbridge = Rlower - Rq
        Rleft = self.Ry + Rp
        Rs = Rr + self.Rdiode
        Rb = Rleft*Rbridge/(Rleft - Rbridge) - Rs

        return Rb

    def synthesis_find_pair(self, Vin_next, m_next):
        '''
        Finds the next pair of resistors, given the next breakpoint voltage
        and the slope to its right. Adds the pair as a stage to the circuit.
        '''
        Ra = self.synthesis_find_Ra(Vin_next)
        Rb = self.synthesis_find_Rb(Ra, m_next)
        self.analysis_add_stage(Ra, Rb)
        return Ra, Rb
        
    def display(self):
        '''
        Displays the current state of the analysis or synthesis
        '''

        for var, val in self.__dict__.items():
            print(f'    {var} = {val}')


# Test of circuit analysis:

Vins = [0]
Vouts = [0]
l = Ladder(Vmax=3, Vref=2.4, Vdiode = 0.55, Rdiode=33, Rin=200, Rtail=331)
for Ra, Rb in [
        (100, 2000),
        (33, 1000),
        (82, 470),
        (47, 330),
        (30, 120),
        (39, 0),
        ]:
    l.analysis_add_stage(Ra, Rb)
    Vins.append(l.Vin_last)
    Vouts.append(l.Vout_last)

Vins.append(l.Vmax_in)
Vout = l.Vout_last + l.m * (l.Vmax_in - l.Vin_last)
Vouts.append(Vout)


# Plot the transfer function
fig=plt.figure(figsize=(8, 4.5), dpi=240)
plt.title('Predicted transfer function of textbook shaper')
plt.plot(Vins, Vouts, 'b+-', ms=10, label='Predicted response')
plt.xlabel('Input Voltage (V)')
plt.ylabel('Output Voltage (V)')
xs = np.linspace(0, l.Vmax_in, 100)
plt.plot(xs, 1.01*l.Vmax_out*np.sin(xs/l.Vmax_out), 'r-', label="Ideal sine curve")
#plt.plot(xs, l.Vmax_out*np.sin(xs/l.Vmax_out), 'r-', label="Ideal sine curve")
plt.legend()

#-----------------------------------------------------------------------------
#
# Run the optimizer
#
#-----------------------------------------------------------------------------

initguess = initial_guess(Vin_max, Vout_max, ndiodes)
print('Initial guess:')
print(initguess)
bounds = param_bounds(Vin_max, ndiodes)
print('Bounds')
print(bounds)
constraints = param_constraints(ndiodes)
print('Constraints:')
print(constraints)

result = scipy.optimize.minimize(objective,
                                 initguess,
                                 args=[Vin_max, Vout_max],
                                 method='SLSQP',
                                 bounds=bounds,
                                 constraints=constraints,
                                 tol=1e-9,
                                 options={'disp': True})

# Report out on the optimization results
print(result)

# What THD did we achieve?
# Sum of squares of harmonics
SSH = result.fun
# Mean square of harmonics
MSH = SSH/l.Vmax_in
# Root mean square harmonics
RMSH = np.sqrt(MSH)
# Root mean square fundamental
RMSF = l.Vmax_out * np.sqrt(2)/2
# Total harmonic distortion
THD = RMSH/RMSF
THD_dB = 20*np.log10(THD)
print(f'Total harmonic distortion (theoretical): {100*THD:.3f}% = {THD_dB:.1f} dB)')

# Unpack optimized parameters
ws = result['x'][0:ndiodes]
ms = result['x'][ndiodes:]
if len(ms) < len(ws):
    ms = np.concatenate([ms, [0]])

# Reconstruct breakpoints, including endpoints
lastw = Vin_max - sum(ws)
ws = np.concatenate([ws, [lastw]])
ms = np.concatenate([[1], ms])
break_xs = np.concatenate([[0], np.cumsum(ws)])
break_ys = np.concatenate([[0], np.cumsum(ms*ws)])
print('    Vin     Vout     Slope')
for x, y, m in zip(break_xs, break_ys, ms):
    print(f'{x:8.3f} {y:8.3f} {m:8.3f}')

# Plot the fitted function
V = sympy.symbols('V')
plt.figure(figsize=(8, 4.5), dpi=240)
title = f'Approximate {f(V, Vout_max)} with a ladder of {ndiodes} diodes'
plt.title(title)
plt.xlabel('Input voltage')
plt.ylabel('Output voltage')
xs = np.linspace(0, Vin_max, 1000)
plt.plot(xs, feval(xs, Vout_max), '-r', label=f'Ideal sine curve')
plt.plot(break_xs, break_ys, '-+b', ms=10, label=f'Best {ndiodes} breakpoints')
plt.legend()
annotation = f'THD = {100*THD:.3f}% ({THD_dB:.1f} dB)'
text_box = AnchoredText(annotation, loc=4, pad=0.5)
plt.setp(text_box.patch, facecolor='white', alpha=0.5)
plt.gca().add_artist(text_box)

# Symthesise a ladder

l = Ladder(Vmax=3, Vref=2.4, Vdiode = 0.55, Rdiode=33,
           Imax=0.005, Iref=0.006)

Rs = []
tail = 0
print(f'Input resistor = {l.Rin}')
for Vin, m in zip(break_xs[1:], ms[1:]):
    Ra, Rb = l.synthesis_find_pair(Vin, m)
    tail += Ra
    Rs.append((Ra, Rb))
print(f'Divider stack sum = {tail}')
print(np.array(Rs))

# Test of circuit synthesis (round resistors to E96):

Rs = [(28.0, 4230.),
      (130., 1870.),
      (93.1, 931.),
      (66.5, 432.),
      (47.5, 154.),
      (34.0, 18.2),
]
Rtail = sum(p[0] for p in Rs)
print('E96 values:')
print('Input resistor: 340')
print(np.array(Rs))
print(f'Sum of lower resistors = {Rtail}')
Vins = [0]
Vouts = [0]
l = Ladder(Vmax=3, Vref=2.4, Vdiode = 0.55, Rdiode=33, Rin=340, Rtail=Rtail)
for Ra, Rb in Rs:
    l.analysis_add_stage(Ra, Rb)
    Vins.append(l.Vin_last)
    Vouts.append(l.Vout_last)
Vins.append(l.Vmax_in)
Vout = l.Vout_last + l.m * (l.Vmax_in - l.Vin_last)
Vouts.append(Vout)

Vins = np.array(Vins)
Vouts = np.array(Vouts)
x0s = Vins[:-1]
ws = Vins[1:] - x0s
y0s = Vouts[:-1]
ms = (Vouts[1:]-y0s)/ws
# Sum of squares of harmonics
SSH = sum(pwl_error_on_interval(x0s, ws, y0s, ms, l.Vmax_out))
# Mean square of harmonics
MSH = SSH/l.Vmax_in
# Root mean square harmonics
RMSH = np.sqrt(MSH)
# Root mean square fundamental
RMSF = l.Vmax_out * np.sqrt(2)/2
# Total harmonic distortion
THD = RMSH/RMSF
THD_db = 20*np.log10(THD)


fig=plt.figure(figsize=(8, 4.5), dpi=240)
plt.title('Predicted transfer function of synthesized shaper')
plt.xlabel('Input Voltage (V)')
plt.ylabel('Output Voltage (V)')
xs = np.linspace(0, l.Vmax_in, 100)
plt.plot(xs, l.Vmax_out*np.sin(xs/l.Vmax_out), 'r-', label="Ideal sine curve")
plt.plot(Vins, Vouts, 'b+-', ms=10, label='Predicted response')
annotation = f'THD = {100*THD:.3f}% ({THD_db:.1f} dB)'
text_box = AnchoredText(annotation, loc=4, pad=0.5)
plt.setp(text_box.patch, facecolor='white', alpha=0.5)
plt.gca().add_artist(text_box)
plt.legend()



# Show the plotted data
plt.show()
