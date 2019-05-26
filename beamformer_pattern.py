from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

import numpy as np
import math
import cmath

class Board:
  def __init__(self,name,n_mics,coordinates):
    self.name = name
    self.n_mics = n_mics
    self.coordinates = coordinates
    self.radius = math.sqrt(coordinates[0]**2 + coordinates[1]**2)/1000
    self.element_distance = 2.0*self.radius*math.sin(math.pi/n_mics)

fs= 48000

sound_speed = 340

creator = Board("Creator",8,[20.0908795,48.5036755])
voice = Board("Voice",7,[-38.13,3.58])

device = creator

print(device.name,"interelement spacing:", device.element_distance*1000,"mm")


def steering_vector(frequency,theta):
  vector = []
  w = 2*math.pi*frequency  
  for i in range(0,device.n_mics):
    phi_angle = (2.0*math.pi*i)/(device.n_mics)
    tau_delay =((device.radius/sound_speed)*math.cos(theta-phi_angle))
    print("---",tau_delay, theta)
    element = cmath.rect(1,w*tau_delay)
    vector.append(element)
  return np.asarray(vector)

def delay_sum_filter(frequency,theta,theta_steer):
  vector = []
  w = 2*math.pi*frequency  
  for i in range(0,device.n_mics):
    phi_angle = (2.0*math.pi*i)/(device.n_mics)
    tau_delay =((device.radius/sound_speed)*math.cos(theta-phi_angle))
    element = (1/device.n_mics)*cmath.rect(1,w*tau_delay)
    vector.append(element)
  return np.asarray(vector)

def filter_result(frequency,angle,steer_angle):
  steer_vector = steering_vector(frequency,angle)
  delay_filter = np.conjugate(delay_sum_filter(frequency,angle,steer_angle))
  operation = np.multiply(delay_filter,steer_vector)
  return(operation)

length = 10
theta = np.linspace(0,2*np.pi,length )
frequency = np.linspace(10, 10000, length)
angle_s =0*math.pi/180
for a in theta:
  filtered_signal = filter_result(frequency[0],a,angle_s)
  print(filtered_signal , a)


'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

P, F = np.meshgrid(theta,frequency)
R = steering_vector(frequency,theta)

X, Y = R*np.cos(P), R*np.sin(P)

# Plot a basic wireframe.
#ax.contour(X,Y,F,300,extend3d='true')
ax.plot_surface(X,Y,F,rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
plt.show()
'''