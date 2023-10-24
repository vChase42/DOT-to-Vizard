from Limb import Limb
from GUI import DOT_Configuration,DOT_Status 
import vizcam
import vizact
import viz
import vizinfo
import vizdlg
import viztask

###
viz.go()
###

env = viz.addChild('Environments/serving_room.osgb')
avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)


bone_list = [
"Bip01 L UpperArm",
"Bip01 L Forearm",
"Bip01 L Hand",
"Bip01 R UpperArm",
"Bip01 R Forearm",
"Bip01 R Hand",
"Bip01 L Thigh",
"Bip01 L Calf",
"Bip01 L Foot",
"Bip01 R Thigh",
"Bip01 R Calf",
"Bip01 R Foot"
]


#EDIT THIS FOR DEFAULT ADDRESSES
bone_addresses = {
    'D4:22:CD:00:57:48' : 'Bip01 R UpperArm',
    'D4:22:CD:00:57:47' : 'Bip01 R Forearm', #Made up address
    'D4:22:CD:00:57:46' : 'Bip01 R Hand',  #Made up address
  }


my_limbs = {}
dot_config_UI = None
sensor_statuses_UI = None


def main(bone_addr_dictionary):
	init_UI_and_Limbs(bone_addr_dictionary)
	#viztask.schedule(main_loop(bone_addr_dictionary))

def init_UI_and_Limbs(my_dictionary):
	#init corner GUI
	
	print("init UI and limbs")
	sensor_statuses_UI = DOT_Status(my_dictionary)
	
	for address, bone in my_dictionary.items():
		new_limb = Limb(address,bone,avatar)
		my_limbs[address] = new_limb
		
		sensor_statuses_UI.add_write_callback(address,new_limb.set_writing)
		sensor_statuses_UI.add_calibrate_callback(address,new_limb.send_calibrate_message)
		

def main_loop(bone_addr_dictionary):
	print("main_loop")
	while True:
		#update UI
		yield viztask.waitTime(10)
	




if __name__ == "__main__":
	dot_config_UI = DOT_Configuration(main,bone_addresses)


