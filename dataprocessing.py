import viz



# data = {} where: timestamp,quatw,quatx,quaty,quatz,freex,freey,freez,ang_vel_x,ang_vel_y,ang_vel_z

def swap_quat(quat):
	x = quat.x
	y = quat.y
	z = quat.z
	w = quat.w
	return viz.Quat(x,z,y,w)
	
	
	

def dataprocess_callback(avatar, limb_bone, data, calibrate_quat):
	
	#print(f"Timestamp: {data['timestamp']}, Quaternion-w: {data['quatw']}")
	
	
	quaternion = viz.Quat(data['quatx'],data['quatz'],data['quaty'],data['quatw'])
	#print(quaternion
	#quaternion = calibrate_quat * quaternion
	#print(quaternion)
	
	#quaternion = swap_quat(quaternion)
	
	limb_bone.setQuat(quaternion,viz.ABS_GLOBAL)
	# hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
