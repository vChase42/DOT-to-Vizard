import viz


# timestamp,quatw,quatx,quaty,quatz,freex,freey,freez,ang_vel_x,ang_vel_y,ang_vel_z

def dataprocess_callback(avatar, limb_bone, data, calibrate_quat):
	
	#print(f"Timestamp: {data_dictionary['timestamp']}, Quaternion-w: {data_dictionary['quatw']}")
	
	
	quaternion = viz.Quat(data['quatw'],data['quatx'],data['quaty'],data['quatz'])
	quaternion = calibrate_quat * quaternion
	limb_bone.setQuat(quaternion, mode = viz.ABS_GLOBAL)
	# hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
