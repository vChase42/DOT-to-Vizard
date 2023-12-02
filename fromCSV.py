from dataprocessing import dataprocess_callback
import csv
import viztask
import viz
import vizcam
import math
import numpy as np

filename = "output_Bip01 L Forearm.csv"         #modify this
limb_name = filename.split('_')[1].split('.')[0]

#limb_name = "Bip01 R Forearm"

avatar = viz.addAvatar('vcc_male2.cfg')
limb_bone = avatar.getBone(limb_name)
limb_bone.lock()


vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)
viz.go()



def main():
	with open(filename, mode='r') as file:
		csv_reader = csv.DictReader(file)
		
		
		test_dic = {
			'quatw': 0.9239,
			'quatx': 0.0,
			'quaty': -0.3827,
			'quatz': 0.0
		}
		
		A = viz.Quat(test_dic['quatx'],test_dic['quaty'],test_dic['quatz'],test_dic['quatw'])
		C = viz.Quat(0,0,0,1)
		
		flag = True
		
		
		for row in csv_reader:
			row_dict = dict(row)
			

			if(flag):
				flag=False
				B = viz.Quat(row_dict['quatx'],row_dict['quaty'],row_dict['quatz'],row_dict['quatw'])
				C = B.inverse() * A
			
			dataprocess_callback(avatar, limb_bone, row_dict, C)
			yield viztask.waitTime(0.01)


quat = viz.Quat(1,0,0,0)
all_attributes = dir(quat)

# Filter and print only the methods
methods = [attr for attr in all_attributes if callable(getattr(quat, attr))]
for method in methods:
    print(method)



if __name__ == "__main__":
	#pass
	viztask.schedule(main())
	#testing()


def testing():
	
	test_dic = {
		'quatw': 0.9239,
		'quatx': 0.0,
		'quaty': 0.3827,
		'quatz': 0.0
	}
	test_quat = viz.Quat(0.0,-0.3827,0.0, 0.9239)
	
	incoming_dic = {
		'quatw': 0.4384231676703282,
		'quatx':  0.7482955650736513,
		'quaty': 0.4554319925956999,
		'quatz': -0.1910514429577342
	
	}
	
	
	random_quat = viz.Quat(0.4384231676703282, 0.7482955650736513, 0.4554319925956999, -0.1910514429577342)
	
	calibrate_quat = test_quat * random_quat.inverse()
				
	dataprocess_callback(avatar, limb_bone, test_dic, viz.Quat(0,0,0,1))
	