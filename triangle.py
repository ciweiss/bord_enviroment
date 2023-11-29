import numpy as np
import math
import matplotlib.pyplot as plt
r_t=1
r_b=2
alpha=30
beta=60
alpha=math.radians(alpha)
beta=math.radians(beta)
s_a=math.sin(alpha)
c_a=math.cos(alpha)
s_b=math.sin(beta)
c_b=math.cos(beta)
rotation=np.array([[c_a,-s_a,0],[s_a*c_b,c_a*c_b,-s_b],[s_a*s_b,c_a*s_b,c_b]])
translation=np.array([[2*r_b*c_a],[2*r_b*s_a*c_b],[2*r_b*s_a*c_b]])
