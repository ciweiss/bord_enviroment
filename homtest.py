import numpy as np
import normal_vectors
import matplotlib.pyplot as plt

r=56.5
h=107
r_rolle=9
list=[1,10,7,4,8,5,2,11,9,6,3,0]
list2=[0,1,2,3,4,5,6,7,8,9,10,11]
arm=normal_vectors.continuum_arm(h,r,r_rolle,12.0,list2)
print(arm.motor_list)
x =arm.triangles_ground[0]
y =arm.triangles_ground[1]
n =arm.motor_list
fig, ax = plt.subplots()
ax.scatter(x, y)

for i, txt in enumerate(n):
    ax.annotate(txt+1, (x[i], y[i]))
print(arm.calc_len())
