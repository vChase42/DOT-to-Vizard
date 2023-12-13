import viz
#import numpy as np
#import quaternion


	#print(f"Timestamp: {data['timestamp']}, Quaternion-w: {data['quatw']}")

def swap_quat(quat):
	x = quat.x
	y = quat.y
	z = quat.z
	w = quat.w
	return viz.Quat(x,z,y,w)
	
def multiply_quaternions(q1, q2):
    x1, y1, z1, w1 = q1.x, q1.y, q1.z, q1.w
    x2, y2, z2, w2 = q2.x, q2.y, q2.z, q2.w

    # Calculate the product components
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2

    return viz.Quat(x, y, z, w)

def inverse(quat):
	x = -quat.x
	y = -quat.y
	z = -quat.z
	w = quat.w
	return viz.Quat(x,y,z,w)
	
	

# data = {} where: timestamp,quatw,quatx,quaty,quatz,freex,freey,freez,ang_vel_x,ang_vel_y,ang_vel_z
def dataprocess_callback(avatar, limb_bone, data, calibrate_quat):
	
	quat = viz.Quat(data['quatx'],data['quatz'],data['quaty'],data['quatw'])
	
	
	#print(quat)
	quat = multiply_quaternions(calibrate_quat,quat)
	
	
	limb_bone.setQuat(quat,viz.ABS_GLOBAL)
	# hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
