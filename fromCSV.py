from dataprocessing import dataprocess_callback
import csv
import viztask
import viz
import vizcam
import math
import numpy as np
import vizshape

avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)
viz.go()

world_axes = vizshape.addAxes()
X = viz.addText3D('X',pos=[1.1,0,0],color=viz.RED,scale=[0.3,0.3,0.3],parent=world_axes)
Y = viz.addText3D('Y',pos=[0,1.1,0],color=viz.GREEN,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
Z = viz.addText3D('Z',pos=[0,0,1.1],color=viz.BLUE,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)

files = []          #Add all limb csv's to this list.

#files.append("data/output_Bip01 L Forearm.csv")
#files.append("data/output_Bip01 L UpperArm.csv")
files.append("data/output_Bip01 R UpperArm.csv")

limb_names = [x.split('_')[1].split('.')[0] for x in files]
limb_bones = [avatar.getBone(x) for x in limb_names]
for limb_bone in limb_bones:
	limb_bone.lock()


#angle = math.radians(45)
#quat = viz.Quat(0, math.sin(angle), 0,math.cos(angle))
quat = viz.Quat(0.0,0.0,0.0, 1.0)         #identity quaternion
quat = viz.Quat(0.0,0.707,0.0, 0.707)       #Calibrate Correction
#quat = viz.Quat(0.707, 0.0, 0.707, 0)
#quat = viz.Quat(-0.5652620637716952, 0.3097127774868339, -0.7630666873549519, 0.04453403112236093)

def read_csv(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def main():
	list_of_csvs = [read_csv(x) for x in files]
		
	count = max([len(x) for x in list_of_csvs])
	print(count)
	
	for i in range(count):
		for ilimb in range(len(list_of_csvs)):
			if(len(list_of_csvs[ilimb]) <= i): continue
			dataprocess_callback(avatar,limb_bones[ilimb],list_of_csvs[ilimb][i],quat)
		yield viztask.waitTime(0.03)
	


if __name__ == "__main__":
	#pass
	viztask.schedule(main())
