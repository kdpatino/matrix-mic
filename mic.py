
import math
import cmath
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

sound_speed = 340

n_mics_creator = 8
n_mics_voice = 7

f=5000
w = 2*math.pi*f


CREATOR = [20.0908795,48.5036755]

size =5000
vector = np.arange(0,size,1)

CREATOR_radius =  math.sqrt(CREATOR[0]**2 + CREATOR[1]**2)/1000
print(CREATOR_radius)

n_mics = n_mics_creator
radius = CREATOR_radius

delta = 2*math.pi*math.sin(math.pi/n_mics)

phi_angle = []
tau_delay = []
output = []
theta = []
steer_vector = []

for a in vector:
    angle = (a*360*math.pi)/(len(vector)*180) #((360*a/size-1)*(math.pi/180))
    theta.append(angle)
    steer = 0
    for i in range(0,n_mics):
        phi_angle = (2*math.pi*i)/(n_mics)
        delta_radius = 2*radius*math.sin(math.pi/n_mics)
        tau_delay =((radius/sound_speed)*math.cos(angle-phi_angle))
        steer += cmath.rect(1,w*tau_delay)
        
        #print(abs(steer))

    output.append(abs(steer))


ax = plt.subplot(111, projection='polar')
ax.plot(theta, output)
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()