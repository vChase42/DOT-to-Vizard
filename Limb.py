from bleak import BleakClient
from dataprocessing import dataprocess_callback
import viz
import math
import asyncio
import numpy as np
import vizcam

import csv

from datetime import datetime
def time_string():
	return "[" + datetime.now().strftime("%H:%S") + "]"

def multiply_quaternions(q1, q2):
    x1, y1, z1, w1 = q1.x, q1.y, q1.z, q1.w
    x2, y2, z2, w2 = q2.x, q2.y, q2.z, q2.w

    # Calculate the product components
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2

    return viz.Quat(x, y, z, w)


class Limb:
    def __init__(self, dot_address, limb_name, avatar, callback_func, write = False):
        self.ACTIVE = True
        
        #limb identification variables
        self.avatar = avatar
        self.limb_name = limb_name
        self.limb_bone = self.avatar.getBone(limb_name)
        self.limb_bone.lock()
        self.dataprocesser_callback = callback_func
        
        #limb coordinate calibration
        self.calibrate_quat = viz.Quat(0,0,0,1)
        self.current_quat = viz.Quat(0,0,0,1)
        
        #Xsens DOT sensor variables
        self.client = BleakClient("00:00:00:00:00:00")  
        self.address = dot_address

        self.measurement_characteristic_uuid = '15172001-4947-11e9-8646-d663bd873d93'
        self.long_payload_characteristic_uuid = '15172002-4947-11e9-8646-d663bd873d93'
        #self.short_payload_characteristic_uuid = "15172004-4947-11e9-8646-d663bd873d93"
        self.binary_message = b"\x01\x01\x1a"  #custommode5

                    
        #file management
        self.writeData = write
        
        #current_time_str = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        self.filename = f"output_{self.limb_name}.csv"
        self.file = None
        self.writer = None        

        #status variables
        self.stream_success = False
        self.status = ["Disconnected"]    #status[0] = Device Valid or Invalid, status[1] = Streaming or Inactive, status[2] = Streaming Mode, status[4] = self.stream_success
        
        #program exit variables
        self.close_success = False
        
        viz.director(self.director_func)  #BEGIN DATA STREAMING


    def notification_callback(self, sender, data):
        self.stream_success = True
        data_dictionary = self.encode_custommode5(data)

        self.current_quat = viz.Quat(data_dictionary['quatx'],data_dictionary['quaty'],data_dictionary['quatz'],data_dictionary['quatw'])
        self.dataprocesser_callback(self.avatar, self.limb_bone, data_dictionary, self.calibrate_quat)
        
        
        if(self.writeData):
            self.write_row_to_file(data_dictionary)


    def encode_custommode5(self, bytes_):
        # These bytes are grouped according to Movella's BLE specification dot
        data_segments = np.dtype([   #the expected data format
            ('timestamp', np.uint32),
            ('quatw', np.float32),
            ('quatx', np.float32),
            ('quaty', np.float32),
            ('quatz', np.float32),
            ('freex', np.float32),
            ('freey', np.float32),
            ('freez', np.float32),
            ('ang_vel_x', np.float32),
            ('ang_vel_y', np.float32),
            ('ang_vel_z', np.float32)
            ])
        
        byte_len = len(bytes_)
        if(byte_len != 63):
            print(f"There are {byte_len} bytes being received, not 44, proceeding anyways")
            print(bytes_)
        try:
            formatted_data = np.frombuffer(bytes_[0:44], dtype=data_segments)
            result_dict = {field: formatted_data[0][field] for field in formatted_data.dtype.names}
        except Exception as e:
            result_dict = {}
            print(f"FAILURE: {e}")
        return result_dict
        

    async def establish_streaming(self):
        try:
            async with BleakClient(self.address) as client:
                print(f"Connection status for client {self.address}: {client.is_connected}") 
                self.client = client
                await client.write_gatt_char(self.measurement_characteristic_uuid,b"\x01\x00\x01", response=True)   #stop streaming
                await asyncio.sleep(1)
                if client.is_connected:
                    await client.start_notify(self.long_payload_characteristic_uuid, self.notification_callback)
                    await client.write_gatt_char(self.measurement_characteristic_uuid, self.binary_message, response=True)   #start streaming

                    while(self.ACTIVE):
                        self.status = await self.get_status_v2()
                        await asyncio.sleep(5)
                    
                    await client.stop_notify(self.long_payload_characteristic_uuid)
                    await client.disconnect()
                    self.file.close()
        except Exception as e:
            print(f"Exception occurred: {e}")
        print(f"Exiting async loop for address {self.address}")


    def director_func(self):
        asyncio.run(self.establish_streaming())
        self.close_success = True
    


    def client_status(self):
        print(f"Client connection: {self.client.is_connected}")
        return self.client.is_connected
    
    
    
    def _initialize_writer(self, my_dictionary):   #if file does not exist, call this
        file_exists = False
        try:
            with open(self.filename, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        self.file = open(self.filename, 'a', newline='',buffering=1)
        self.writer = csv.DictWriter(self.file, fieldnames=list(my_dictionary.keys()))
        
        if not file_exists:
            self.writer.writeheader()

    def write_row_to_file(self, my_dictionary):
        if self.writer is None:
            self._initialize_writer(my_dictionary)

        self.writer.writerow(my_dictionary)
        
    def send_calibrate_message(self):
        desired_quat = viz.Quat(0.0,0,0.0,1)

        self.calibrate_quat = multiply_quaternions(desired_quat, self.current_quat.inverse())
        
        
        #if(self.client.is_connected):
        #    asyncio.run(self.async_send_calibrate_message())
        #else:
        #    print("Client not connected")
        
    async def async_send_calibrate_message(self):
        calibrate_message = b"\x00\x01"
        calibrate_characteristic_uuid = "15172006-4947-11e9-8646-d663bd873d93"

        await self.client.write_gatt_char(calibrate_characteristic_uuid , calibrate_message, response=True)
        print("Calibration message sent")
        
    
    def set_writing(self,value):
        print("Streaming data will now be written to file:",value)
        self.writeData = value
        
    def close(self):
        self.writeData = False
        self.ACTIVE = False
        
    def is_closed(self):
        return self.close_success
        
    async def get_status_v2(self):
        #b"\x01\x01\x05"
        if(not self.client.is_connected):
            return ["Disconnected"]
        message = await self.client.read_gatt_char(self.measurement_characteristic_uuid)
        return self.parse_gatt_message(message)
        
    def parse_gatt_message(self,data):
        if len(data) != 3:
            raise ValueError("Invalid data length. Expected 3 bytes.")

        # Parsing each byte
        type_byte = data[0]
        action_byte = data[1]
        payload_mode_byte = data[2]

        # Parsing the Type
        if type_byte == 1:
            type_description = "Valid"
        else:
            type_description = "Invalid Value"

        # Parsing the Action
        if action_byte == 0:
            action_description = "Inactive"
        elif action_byte == 1:
            action_description = "Measuring"
        else:
            action_description = "Invalid Action"

        # Parsing the Payload Mode
        payload_mode_descriptions = {
            1: "High Fidelity (with mag) 1",
            2: "Extended (Quaternion)",
            3: "Complete (Quaternion)",
            4: "Orientation (Euler)",
            5: "Orientation (Quaternion)",
            6: "Free acceleration",
            7: "Extended (Euler)",
            16: "Complete (Euler)",
            17: "High Fidelity 2",
            18: "Delta quantities (with mag)",
            19: "Delta quantities",
            20: "Rate quantities (with mag)",
            21: "Rate quantities",
            22: "Custom mode 1",
            23: "Custom mode 2",
            24: "Custom mode 3",
            25: "Custom mode 4",
            26: "Custom mode 5"
        }
        payload_mode_description = payload_mode_descriptions.get(payload_mode_byte, "Invalid Payload Mode")
        print(time_string(),f"State: {type_description}, Action: {action_description}, Mode: {payload_mode_description}")
        return [type_description, action_description, payload_mode_description, self.stream_success]
        
    
if __name__ == "__main__":
    viz.go()
    #env = viz.addChild('Environments/serving_room.osgb')
    avatar = viz.addAvatar('vcc_male2.cfg')
    vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)

    address = "D4:22:CD:00:57:48" # Movella DOT UUID
    body_part = 'Bip01 R UpperArm'
    
    my_limb = Limb(address,body_part,avatar, dataprocess_callback)

