from Space import Space
from SystemState import SystemState
from RK4Stepper import RK4Stepper
from ODESolver import ODESolver
import random
import numpy as np
import matplotlib.pyplot as plt
def getStartingState(zcoord):
    return SystemState(
        EarthPosition=[-3.1617821569319294E10, 1.436603570949401E11, 117565.96043321176],
        EarthVelocity=[-29581.545053209236, -6515.282025813395, -0.010617114855559093],
        AsteroidPosition=[-1.59458654e+11, -1.94077604e+11,  6.61733278e+09],
        AsteroidVelocity=[13224.513110762178, -14246.151046842608, zcoord]
    )

space = Space()
stepper = RK4Stepper()
solver = ODESolver(stepper, space)
def printer(time, state, iteration):
    pass
    #print(state)

solver.registerOutput(printer)
a = []
b = []
for an in range(350,400):
    # 758 +- 30; 1000 iterací
    #z = random.gauss(758, 37.9) # 5%
    #z = an*2
    hit, smallest_spd = solver.integrate(0, 365*24*60*60, 5*60, 10E-6, getStartingState(z))
    a.append(smallest_spd)
    b.append(z)
print(a)
print(b)
# 750 - 800
def gravitacni_zrychleni(m2, p1, p2):
    zrychleni = GConst * m2/(p1 - p2)**2

    return zrychleni
