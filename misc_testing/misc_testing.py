import viz
import vizact
import viztask
import vizcam
import math
import vizshape


#byte = b'\xe3\xb4\xee\x13[\xc9\x81=D\t-?\xe4Z\xe5=V\xc49\xbf\x8c3\xd5\xbe\xbf\xde\xe4>\xf5>\x1eATj\x99\xc0}Y\x0c\xbe\x06)&?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'



#print(len(byte))

#print(byte[0:44])

world_axes = vizshape.addAxes()
X = viz.addText3D('X',pos=[1.1,0,0],color=viz.RED,scale=[0.3,0.3,0.3],parent=world_axes)
Y = viz.addText3D('Y',pos=[0,1.1,0],color=viz.GREEN,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
Z = viz.addText3D('Z',pos=[0,0,1.1],color=viz.BLUE,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)


avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)
viz.go()

limb_name = "Bip01 R UpperArm"
limb_bone = avatar.getBone(limb_name)
limb_bone.lock()

#w,x,y,z
quat = viz.Quat(-0.13989022,-0.25052834,0.93941283,-0.18753815)
cal_quat = viz.Quat(0.0,-0.707,0.0, 0.707)
#cal_quat = viz.Quat(0,0,0,1)


#desired_quat = viz.Quat(0.0,-0.707,0.0, 0.707)

#cal_quat = desired_quat * quat.inverse()
#print(cal_quat)
#print(cal_quat.inverse())

quat = cal_quat * quat
quat = cal_quat * quat * cal_quat.inverse()

limb_bone.setQuat(quat,viz.ABS_GLOBAL)