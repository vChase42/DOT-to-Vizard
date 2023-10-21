import viz
import vizinfo
import vizdlg
import vizact

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



class DOT_Configuration:
	def __init__(self, call_back_func, addr_bone_dic):
		self.my_panel = vizinfo.InfoPanel('Added Devices.',title='BLE Configuration', align=viz.ALIGN_CENTER_CENTER, icon=False) #init panel
		self.sensors = []

		self.populate_panel()

		#add config address-bone pairs
		for key,value in addr_bone_dic.items():
			print(key,value)
			self.add_sensor(key,value)
		
		self.done_func = call_back_func

	def populate_panel(self):

		self.my_panel.addSeparator()
		
		#Header
		dlg_header = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		dlg_header.addItem(viz.addText('Address                   Body Part                        Enabled'))
		self.my_panel.addItem(dlg_header)
		self.my_panel.addSeparator()
		
		#Address-Bone Pairs
		self.dlg_sensors = vizdlg.Panel(layout=vizdlg.LAYOUT_VERT_LEFT, border=False,background=False,margin=0)
		self.my_panel.addItem(self.dlg_sensors)
		
		#Add Button
		add_device_button = self.my_panel.addItem(viz.addButtonLabel('Add Device'),align=viz.ALIGN_RIGHT_CENTER)
		
		#Done Button
		self.my_panel.addSeparator()
		done_button = self.my_panel.addItem(viz.addButtonLabel('Connect and Begin Streaming'),align=viz.ALIGN_LEFT_CENTER)
		
		
		vizact.onbuttonup(add_device_button,self.create_add_device_window)
		vizact.onbuttonup(done_button,self.done_configuration)
		
		
	def add_sensor(self,address,body_part):
		dlg_sensor = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)

		#Textbox
		dlg_sensor.addItem(viz.addText(address),align=viz.ALIGN_CENTER_CENTER)
		
		#Dropdown
		dropdown = dlg_sensor.addItem(viz.addDropList())
		dropdown.addItems(bone_list)
		dropdown.select(bone_list.index(body_part))
		
		#Enable/Disable 
		checkbox = dlg_sensor.addItem(viz.addCheckbox(),align=viz.ALIGN_CENTER_CENTER)
		checkbox.set(viz.DOWN)
		
		#Remove
		remov_button = dlg_sensor.addItem(viz.addButtonLabel('Remove'))
		vizact.onbuttonup(remov_button,self.remove_sensor,dlg_sensor)
		
		#record data
		self.dlg_sensors.addItem(dlg_sensor)
		self.sensors.append(dlg_sensor)
	
	def remove_sensor(self,dlg_obj):
		self.sensors.remove(dlg_obj)
		dlg_obj.remove()
		
	def create_add_device_window(self):
		self.configureWindow = viz.addWindow(size=(1,1), pos=(0,1), clearMask = 0, scene=viz.addScene())
		configurePanel = vizinfo.InfoPanel('Input XSENS DOT address',title='Configure XSENSE DOT', window = self.configureWindow ,align=viz.ALIGN_CENTER_TOP, icon=False)
		config_row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False)
		configurePanel.addItem(config_row)
		
		#textbox
		config_row.addItem(viz.addTextbox())
		#dropdown
		dropdown = config_row.addItem(viz.addDropList())
		dropdown.addItems(bone_list)
		
		done_button = configurePanel.addItem(viz.addButtonLabel('Add'))
		vizact.onbuttonup(done_button,self.done_device_window, config_row)
		
	def done_device_window(self, row):
		address = row.getChildren()[2].get()
		body_part = bone_list[row.getChildren()[3].getSelection()]
		
		self.add_sensor(address,body_part)
		self.configureWindow.remove()
		
	def done_configuration(self):
		active_sensors = [x for x in self.sensors if x.getChildren()[4].get() == 1]
		
		new_dictionary = {}
		for sensor in active_sensors:	
			dlg_obj = sensor.getChildren()
			address = dlg_obj[2].getMessage()
			body_part = bone_list[dlg_obj[3].getSelection()]
			
			new_dictionary[address] = body_part
		#print("configuration sent", new_dictionary)
		self.done_func(new_dictionary)
		self.my_panel.remove()

addr_bone_dic = {
	"00:00:00:00:00:00":"Bip01 R Foot",
	"01:00:00:00:00:00":"Bip01 R UpperArm",
	"02:00:00:00:00:00":"Bip01 R Hand",
}
def print_addresses(my_dictionary):
	print("SELECTED ADDRESS-BODY_PART PAIRS:")
	for key,bone in my_dictionary.items():
		print(key,bone)
	

if __name__ == "__main__":
	viz.go()
	my_config = DOT_Configuration(print_addresses,addr_bone_dic)


