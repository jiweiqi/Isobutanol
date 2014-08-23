"""
Constant-pressure, adiabatic kinetics simulation.
"""

import sys
import numpy as np

import cantera as ct

gri3 = ct.Solution('mit_2013_chem.xml')
air = ct.Solution('air.xml')

P_eff = 25/1.013
for T_eff in range(800,1000,+20):
    gri3.TPX = T_eff, P_eff*ct.one_atm, 'iBuOH:0.4,O2:6,N2:43.56'
    r = ct.IdealGasReactor(gri3,verbose=1)
    env = ct.Reservoir(air)

    # Define a wall between the reactor and the environment, and
    # make it flexible, so that the pressure in the reactor is held
    # at the environment pressure.
    w = ct.Wall(r, env)
    w.expansion_rate_coeff = 0.0  # set expansion parameter. dV/dt = KA(P_1 - P_2)
    w.area = 1.0

    N = 40000
    sim = ct.ReactorNet([r])
    time = 0.0
    times = np.zeros(N)
    data = np.zeros((N,4))

    ##print('%10s %10s %10s %14s' % ('t [s]','T [K]','P [Pa]','u [J/kg]'))
    for n in range(N):
        time += 1.e-5 
        sim.advance(time)
        times[n] = time * 1e3  # time in ms
        data[n,0] = r.T
        data[n,1:] = r.thermo['OH','H','H2'].X
    ##    print('%10.3e %10.3f %10.3f %14.6e' % (sim.time, r.T,
    ##                                           r.thermo.P, r.thermo.u))
        if r.T > T_eff + 200.0:
            print('T=%10.3e [K] Ignition Delay = %10.3e [ms]'% (T_eff,sim.time*1000))
            break

### Plot the results if matplotlib is installed.
### See http://matplotlib.org/ to get it.
##if '--plot' in sys.argv[1:]:
##    import matplotlib.pyplot as plt
##    plt.clf()
##    plt.subplot(2, 2, 1)
##    plt.plot(times, data[:,0])
##    plt.xlabel('Time (ms)')
##    plt.ylabel('Temperature (K)')
##    plt.subplot(2, 2, 2)
##    plt.plot(times, data[:,1])
##    plt.xlabel('Time (ms)')
##    plt.ylabel('OH Mole Fraction')
##    plt.subplot(2, 2, 3)
##    plt.plot(times, data[:,2])
##    plt.xlabel('Time (ms)')
##    plt.ylabel('H Mole Fraction')
##    plt.subplot(2, 2, 4)
##    plt.plot(times,data[:,3])
##    plt.xlabel('Time (ms)')
##    plt.ylabel('H2 Mole Fraction')
##    plt.tight_layout()
##    plt.show()
##else:
##    print("To view a plot of these results, run this script with the option --plot")
