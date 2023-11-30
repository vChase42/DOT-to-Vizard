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
		
		A = viz.Quat(test_dic['quatw'],test_dic['quatx'],test_dic['quaty'],test_dic['quatz'])
		C = viz.Quat(1,0,0,0)
		
		flag = True
		
		
		for row in csv_reader:
			row_dict = dict(row)
			

			if(flag):
				flag=False
				B = viz.Quat(row_dict['quatw'],row_dict['quatx'],row_dict['quaty'],row_dict['quatz'])
				C = B.inverse() * A
			
			dataprocess_callback(avatar, limb_bone, row_dict, C)
			yield viztask.waitTime(0.1)


quat = viz.Quat(1,0,0,0)
all_attributes = dir(quat)

# Filter and print only the methods
methods = [attr for attr in all_attributes if callable(getattr(quat, attr))]
for method in methods:
    print(method)



if __name__ == "__main__":
	#pass
	viztask.schedule(main())
	

	
	#test_dic = {
	#	'quatw': 0.9239,
	#	'quatx': 0.0,
	#	'quaty': -0.3827,
	#	'quatz': 0.0
	#}
				
				
				
	#dataprocess_callback(avatar, limb_bone, test_dic)
	