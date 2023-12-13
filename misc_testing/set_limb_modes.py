import viz
import vizact
import vizcam
import viztask



avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)
viz.go()

limb_name = "Bip01 L UpperArm"
limb_bone = avatar.getBone(limb_name)
limb_bone.lock()

#quat = viz.Quat(0.0,0.3827,0.0, 0.9239)    #45 degree angle rotation
quat = viz.Quat(0.0,0.0,0.0, 1.0)         #identity quaternion
#quat = viz.Quat(0.0,-7.07,0.0, 7.07)         #identity quaternion

viz_constants = [
    viz.ABS_PARENT,    # Perform the transformation absolutely in the bones local coordinate system.
    viz.ABS_GLOBAL,    # Perform the transformation absolutely in the bones global coordinate system.
    viz.ABS_LOCAL,     # Perform the transformation absolutely in the bones local coordinate system.
    viz.REL_LOCAL,     # Perform the transformation relatively in the bones local coordinates system.
    viz.REL_PARENT,    # Perform the transformation relatively in parent bones coordinate system.
    viz.REL_GLOBAL,    # Perform the transformation relatively in bones global coordinate system.
    viz.AVATAR_LOCAL,  # Perform the transformation absolutely in the avatars local coordinate system.
    viz.AVATAR_WORLD   # Perform the transformation absolutely in the avatars global coordinate system.
]


def main():

	for m in viz_constants:
	
		limb_bone.setQuat(quat,viz.ABS_GLOBAL)
		print("Current mode:",m)
		yield viztask.waitTime(2)



viztask.schedule(main)