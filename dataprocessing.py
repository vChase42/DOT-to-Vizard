


def dataprocess_callback(avatar, limb_bone, data):
	
	#print(f"Timestamp: {data_dictionary['timestamp']}, Quaternion-w: {data_dictionary['quatw']}")
	quaternion = viz.Quat(data_dictionary['quatw'],data_dictionary['quatx'],data_dictionary['quaty'],data_dictionary['quatz'])
	self.limb_bone.setQuat(quaternion)
	# hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
