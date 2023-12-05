import viz



# data = {} where: timestamp,quatw,quatx,quaty,quatz,freex,freey,freez,ang_vel_x,ang_vel_y,ang_vel_z

def dataprocess_callback(avatar, limb_bone, data, calibrate_quat):
	
	#print(f"Timestamp: {data['timestamp']}, Quaternion-w: {data['quatw']}")
	
	
	quaternion = viz.Quat(data['quatx'],data['quaty'],data['quatz'],data['quatw'])
	#print(quaternion)
	quaternion = calibrate_quat * quaternion
	#print(quaternion)
	limb_bone.setQuat(quaternion)
	# hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
