import numpy as np
import math
import cmath

import matplotlib
import matplotlib.pyplot as plt


class Board:
  def __init__(self,name,n_mics,coordinates):
    self.name = name
    self.n_mics = n_mics
    self.coordinates = coordinates
    self.radius = math.sqrt(coordinates[0]**2 + coordinates[1]**2)/1000
    self.element_distance = 2.0*self.radius*math.sin(math.pi/n_mics)

fs= 48000

sound_speed = 340

creator = Board("Creator",3,[20.0908795,48.5036755])
voice = Board("Voice",7,[-38.13,3.58])

device = voice

#print(phi_vector)

f = 1
print(device.radius)
wf =2.0*np.pi*f
w_cm = wf*device.radius/sound_speed
print(w_cm)
phi_vector = np.linspace(0, 2*np.pi, device.n_mics+1)
print(phi_vector)
theta_vector = [0,np.pi/2,2*np.pi/3,np.pi]
#theta_vector = [0,np.pi/2]
#A = np.array()
a = []
for theta in theta_vector:
  r = []
  for phy in range(0,device.n_mics):
    item = cmath.rect(1,-w_cm*np.cos(theta-phi_vector[phy]))
    r.append(item)
  a.append(r)

#c1 =[complex(0,0),complex(1,0),complex(-1,0)]
c1 =[complex(0,0),complex(1,0),complex(0,0),complex(0,0),complex(0,0),complex(0,0),complex(-1,0)]
c2 =[complex(0,0),complex(0,0),complex(1,0),complex(0,0),complex(0,0),complex(-1,0),complex(0,0)]
c3 =[complex(0,0),complex(0,0),complex(0,0),complex(1,0),complex(-1,0),complex(0,0),complex(0,0)] 
a.append(c1)
a.append(c2)
a.append(c3)
beta_vector = [1,0,0,0,0,0,0]
#beta_vector = [1,0,0]

A = np.array(a)
#print(A)
A_i = np.linalg.inv(A)
B = np.transpose(beta_vector)
H = np.matmul(A_i,B)
print(A)

def steering_vector(frequency,theta):
  vector = []
  w = 2*math.pi*frequency  
  for i in range(0,device.n_mics):
    tau_delay =(w*(device.radius/sound_speed)*math.cos(theta-phi_vector[i]))
    element = cmath.rect(1,tau_delay)
    vector.append(element)
  return np.asarray(vector)

def filter_result(frequency,angle,steer_angle):
  steer_vector = np.asmatrix(steering_vector(frequency,angle))
  str_T = np.transpose(steer_vector)
  operation = np.matmul(str_T.H,H)
  return(np.asarray(operation))

length = 1000
theta = np.linspace(0,2*np.pi,length )
frequency = np.linspace(10, 10000, length)

data = []
for a in theta:
  result =filter_result(f,a,angle_s)
  data.append(20*np.log10(abs(result[0][0])))

print(data)
ax = plt.subplot(111, projection='polar')

ax.plot(theta, data)
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()