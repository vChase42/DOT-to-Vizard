from Limb import Limb
from GUI import DOT_Configuration 
import vizcam
import vizact
import viz
import vizinfo
import vizdlg

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



bone_addresses = {
    'D4:22:CD:00:57:48' : 'Bip01 R UpperArm',
    'D4:22:CD:00:57:47' : 'Bip01 R Forearm', #Made up address
    'D4:22:CD:00:57:46' : 'Bip01 R Hand',  #Made up address
  }


my_limbs = {}

def init_bones(my_dictionary):
	for address, bone in my_dictionary.items():
		my_limbs[bone] = Limb(address,bone,avatar)	




if __name__ == "__main__":
	DOT_Configuration(init_bones,bone_addresses)


