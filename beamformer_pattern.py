'''
=================
3D wireframe plot
=================

A very basic demonstration of a wireframe plot.
'''

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

import numpy as np
import math
import cmath

sound_speed = 340

n_mics_creator = 8
n_mics_voice = 7

CREATOR = [20.0908795,48.5036755]
CREATOR_radius =  math.sqrt(CREATOR[0]**2 + CREATOR[1]**2)/1000
print(CREATOR_radius)

n_mics = n_mics_creator
radius = CREATOR_radius

delta = 2*math.pi*math.sin(np.pi/n_mics)

def mag_delay(theta , frequency):
  vector = []
  for f in frequency:
    acc = []
    w = 2*math.pi*f
    for angle in theta:
      steer = 0
      for i in range(0,n_mics):
        phi_angle = (2*math.pi*i)/(n_mics)
        #delta_radius = 2*radius*math.sin(math.pi/n_mics)
        tau_delay =((radius/sound_speed)*math.cos(angle-phi_angle))
        steer += cmath.rect(1,w*tau_delay)
      db = 20*math.log10(abs(steer)/n_mics)
      acc.append(db)
    vector.append(acc)
  return np.asarray(vector)

length = 50
theta = np.linspace(0,2*np.pi,length )
frequency = np.linspace(8000, 10000, length)
mag = mag_delay(theta,frequency)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

P, F = np.meshgrid(theta,frequency)
R = mag_delay(theta, frequency)

Y, X = R*np.cos(P), R*np.sin(P)

# Plot a basic wireframe.
ax.plot_surface(X, Y,F, cmap=plt.cm.YlGnBu_r)
plt.show()