from Limb import Limb
from GUI import DOT_Configuration,DOT_Status 
from dataprocessing import dataprocess_callback
import vizcam
import vizact
import viz
import vizinfo
import vizdlg
import viztask
import asyncio

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
#    'D4:22:CD:00:57:47' : 'Bip01 R Forearm', #Made up address
#    'D4:22:CD:00:57:46' : 'Bip01 R Hand',  #Made up address
  }


my_limbs = {}
dot_config_UI = None
sensor_statuses_UI = None
ACTIVE = True

def exit_callback():
	global ACTIVE
	print("Exiting")
	ACTIVE = False

def start_configuration(addr_bone_dictionary):      #this function is called after "Connect and Begin Streaming" button is pressed
	init_UI_and_Limbs(addr_bone_dictionary)
	viztask.schedule(main_loop(addr_bone_dictionary))

def init_UI_and_Limbs(my_dictionary):    #This creates the corner UI
	global sensor_statuses_UI
	
	sensor_statuses_UI = DOT_Status(my_dictionary)
	
	for address, bone in my_dictionary.items():
		new_limb = Limb(address,bone,avatar, dataprocess_callback)
		my_limbs[address] = new_limb
		
		sensor_statuses_UI.add_write_callback(address,new_limb.set_writing)
		sensor_statuses_UI.add_calibrate_callback(address,new_limb.send_calibrate_message)
		sensor_statuses_UI.add_exit_callback(exit_callback)


def update_status(address, UI):
	curr_status = my_limbs[address].status
	status = ""
	
	if(curr_status[0] == "Disconnected"):
		status = "Disconnected"
	elif(curr_status[0] == "Valid"):
		status = "Connected"
		if(curr_status[3] and curr_status[1] == "Measuring"):
			status = "Streaming"
	UI.set_status_text(address,status)

def main_loop(addr_bone_dictionary):    #this is a loop that updates the corner UI with the status of bluetooth devices every 10 seconds
	global sensor_statuses_UI
	yield viztask.waitTime(1.5)

	while ACTIVE:
		#update UI
		
		for address,bone in addr_bone_dictionary.items():
			update_status(address,sensor_statuses_UI)

		yield viztask.waitTime(5)
	print("Exiting(2)")
	#EXIT THE SCRIPT GRACEFULLY
	for address,bone in addr_bone_dictionary.items():
		my_limbs[address].close()

	for address,bone in addr_bone_dictionary.items():
		while not my_limbs[address].is_closed():
			pass

	viz.quit()


if __name__ == "__main__":
	dot_config_UI = DOT_Configuration(start_configuration,bone_addresses)


