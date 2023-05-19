# An example of a nearly SOLID approach to working with ODs in a physics context.

# code should be mostly self-explanatory, and was done as an exercise to see how ideas I 
# use in other languages work in python

# Note: help was obtained from ChatGPT for the type conformance used here.

import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod

class Addable(ABC):
    @abstractmethod
    def __add__(self, other):
        if not isinstance(other, Addable):
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(type(self).__name__, 
                                                                                      type(other).__name__))

class FloatMultiplable(ABC):
    @abstractmethod
    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError("Unsupported operand type(s) for *: '{}' and '{}'".format(type(self).__name__, 
                                                                                      type(other).__name__))

class Integratable(Addable,FloatMultiplable):
    pass
 

class DynamicalSystem(ABC):

    state: Integratable
    time: float

    @abstractmethod
    def dervatives(self, x: Integratable, t: float):
        raise NotImplementedError
 
    
    def euler_step(self, dt: float):
        self.state += self.dervatives(self.state,self.time) * dt
    
    def rk4_step(self, dt: float):

        h = dt # only to make notation the same as numerical recipies
        y = self.state
        t = self.time

        dydx = self.dervatives(y, t)

        hh = h / 2.0
        h6 = h / 6.0
        xh = t + hh
        yt = y + dydx * hh

        dyt = self.dervatives(yt,xh)
        
        yt = y + dyt * hh
        
        dym = self.dervatives(yt, xh)
        
        yt =  y + dym * h 
        
        dym =  dym + dyt 
        dyt = self.dervatives(yt, t + h)

        self.state =  y + ( dydx + dyt + dym * 2.0 ) * h6


class OneDimensionalSystem(Integratable):

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        

    def __add__(self, other):
        if not isinstance(other, OneDimensionalSystem):
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(type(self).__name__, 
                                                                                      type(other).__name__))
        return OneDimensionalSystem(self.position + other.position, 
                                    self.velocity + other.velocity)
        
    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError("Unsupported operand type(s) for *: '{}' and '{}'".format(type(self).__name__, 
                                                                                      type(other).__name__))
        return OneDimensionalSystem(self.position * other, 
                                    self.velocity * other)

class HarmonicOscillator(DynamicalSystem):
    state: OneDimensionalSystem

    # using standrad otation for universal oscillator equation
    def __init__(self, 
                 omega      = 1.0, 
                 zeta       = 0.1, 
                 position   = 1.0, 
                 velocity   = 0.0, 
                 time       = 0.0):
        self.omega = omega
        self.zeta = zeta
        self.state = OneDimensionalSystem(position,velocity)
        self.time = time
        
    def dervatives(self, state, time):
        # not bothered with a drive so no time here
        x = state.position
        v = state.velocity

        dxdt = v
        dvdt = -2.0 * self.zeta * self.omega * v - self.omega * self.omega * x
        
        return OneDimensionalSystem(dxdt,dvdt)


dt = 0.01
tmax = 100.0
nsteps = int(tmax / dt)

sho = HarmonicOscillator()

# Initialize the arrays for position and velocity
x = np.zeros(nsteps)
v = np.zeros(nsteps)

# Set the initial conditions
x[0] = sho.state.position
v[0] = sho.state.velocity

for i in range(1, nsteps):
 #   sho.rk4_step(dt)
    sho.euler_step(dt)
    x[i] = sho.state.position
    v[i] = sho.state.velocity

# Plot the position and velocity as a function of time
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

ax[0].plot(np.arange(nsteps)*dt, x)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Position')

ax[1].plot(np.arange(nsteps)*dt, v)
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Velocity')

plt.show()

# Copyright Mark Everitt 2023 under GNU General Public License v3.0

