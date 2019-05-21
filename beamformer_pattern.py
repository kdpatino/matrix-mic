from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

import numpy as np
import math
import cmath

fs= 48000

sound_speed = 340

n_mics_creator = 8
n_mics_voice = 6

CREATOR = [20.0908795,48.5036755]
VOICE = [-38.13,3.58]
BOARD = VOICE
BOARD_radius =  math.sqrt(BOARD[0]**2 + BOARD[1]**2)/1000

n_mics = n_mics_voice
radius = BOARD_radius

delta = 2*math.pi*math.sin(np.pi/n_mics)
angle_s = 0
def mag_delay(theta , frequency):
  vector = []
  for f in frequency:
    acc = []
    w = 2*math.pi*f
    for angle in theta:
      #print("-------------- ",f ,angle*180/math.pi)
      steer = 0
      for i in range(0,n_mics):
        phi_angle = (2.0*math.pi*i)/(n_mics)
        delta_radius = 2.0*radius*math.sin(math.pi/n_mics)
        tau_delay =((radius/sound_speed)*math.cos(angle-phi_angle))
        tau_delay_s =((radius/sound_speed)*math.cos(angle_s-phi_angle))
        #print(tau_delay*fs)
        #print(cmath.rect(1,w*tau_delay)*cmath.rect(1,w*tau_delay*-1))
        steer += cmath.rect(1,w*tau_delay)*cmath.rect(1,w*tau_delay_s*-1)
      steer += cmath.rect(1,0)
      steer_abs = abs(steer)/float(n_mics+1)
      print("---------------",steer,steer_abs)
      db = 20*math.log10(steer_abs)
      acc.append(steer_abs)
    vector.append(acc)
  return np.asarray(vector)

length = 50
theta = np.linspace(0,2*np.pi,length )
frequency = np.linspace(10, 10000, length)
mag = mag_delay(theta,frequency)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

P, F = np.meshgrid(theta,frequency)
R = mag_delay(theta, frequency)

X, Y = R*np.cos(P), R*np.sin(P)

# Plot a basic wireframe.
#ax.contour(X,Y,F,300,extend3d='true')
ax.plot_surface(X,Y,F,rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
plt.show()