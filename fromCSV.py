from dataprocessing import dataprocess_callback
import csv
import viztask
import viz
import vizcam
import math
import numpy as np

avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)
viz.go()



files = []          #Add all limb csv's to this list.

files.append("data/output_Bip01 L Forearm.csv")               
files.append("data/output_Bip01 L UpperArm.csv")

limb_names = [x.split('_')[1].split('.')[0] for x in files]
limb_bones = [avatar.getBone(x) for x in limb_names]
for limb_bone in limb_bones:
	limb_bone.lock()



def read_csv(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def main():
	list_of_csvs = [read_csv(x) for x in files]
		
	test_dic = {
		'quatw': 0.9239,
		'quatx': 0.0,
		'quaty': -0.3827,
		'quatz': 0.0
	}
	
	A = viz.Quat(test_dic['quatx'],test_dic['quaty'],test_dic['quatz'],test_dic['quatw'])
	C = []
		
	for limb in list_of_csvs:
		B = viz.Quat(limb[0]['quatx'],limb[0]['quaty'],limb[0]['quatz'],limb[0]['quatw'])
		C.append(B.inverse() * A)
	

	count = max([len(x) for x in list_of_csvs])
	print(count)
	
	for i in range(count):
		for ilimb in range(len(list_of_csvs)):
			if(len(list_of_csvs[ilimb]) <= i): continue
			dataprocess_callback(avatar,limb_bones[ilimb],list_of_csvs[ilimb][i],C[ilimb])
		yield viztask.waitTime(0.01)
	


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
	