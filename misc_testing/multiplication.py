import viz
import math
import numpy as np
import quaternion  # This imports the numpy quaternion library

# Define two quaternions
q1 = np.quaternion(1, 2, 3, 4)
q2 = np.quaternion(5, 6, 7, 8)

# Multiply the quaternions
result = q1 * q2

# Print the result
print("Result of numpy quaternion multiplication (w,x,y,z):", result)



v1 = viz.Quat(2,3,4,1)
v2 = viz.Quat(6,7,8,5)

vresult = v1 * v2




def multiply_quaternions(q1, q2):
    x1, y1, z1, w1 = q1.x, q1.y, q1.z, q1.w
    x2, y2, z2, w2 = q2.x, q2.y, q2.z, q2.w

    # Calculate the product components
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2

    return viz.Quat(x, y, z, w)


vresult2 = multiply_quaternions(v1,v2)

print("Manual multiplication of vizard quaternions: (x,y,z,w)",vresult2)
print("Vizard result of multiplication (x,y,z,w):", vresult)

