from bleak import BleakClient
import viz
import math
import asyncio
import numpy as np

import csv




class Limb:
    def __init__(self, dot_address, limb_name, avatar, write = False):
        self.avatar = avatar
        self.limb_name = limb_name
        self.limb_bone = self.avatar.getBone(limb_name)
        self.limb_bone.lock()
        
        self.client = BleakClient("00:00:00:00:00:00")  #hardcoded in case of client_status() call
        self.address = dot_address

        self.measurement_characteristic_uuid = '15172001-4947-11e9-8646-d663bd873d93'
        self.long_payload_characteristic_uuid = '15172002-4947-11e9-8646-d663bd873d93'
        self.binary_message = b"\x01\x01\x26"  #custommode5
            
        self.max_timestamp = 0
        
        self.writeData = write
        self.filename = f"output_{self.limb_name}.csv"
        self.file = None
        self.writer = None        

        
        print(limb_name)
        viz.director(self.director_func)  #BEGIN DATA STREAMING


    def notification_callback(self, sender, data):
        
        data_dictionary = self.encode_custommode5(data)[0]
        #print(f"Timestamp: {data_dictionary['timestamp']}, Quaternion-w: {data_dictionary[quatw]}")
        quaternion = viz.Quat(data_dictionary['quatw'],data_dictionary['quatx'],data_dictionary['quaty'],data_dictionary['quatz'])
        self.avatar.setQuat(quaternion)
        # hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))
        
        if(self.writeData):
            self.write_row_to_file(data_dictionary)


    def encode_custommode5(self, bytes_):
        # These bytes are grouped according to Movella's BLE specification doc
        
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
        if(byte_len != 44):
            print(f"There are {byte_len} bytes being received, not 44, proceeding anyways")
        try:
            formatted_data = np.frombuffer(bytes_[0:44], dtype=data_segments)
        except Exception as e:
            print(f"FAILURE: {e}")
        
        return formatted_data
        
        

    async def establish_streaming(self):
        try:
            async with BleakClient(self.address) as client:
                print(f"Connection status for client {address}: {client.is_connected}") 
                self.client = client
                await asyncio.sleep(1)
                if client.is_connected:
                    await client.start_notify(self.long_payload_characteristic_uuid, self.notification_callback)
                    await client.write_gatt_char(self.measurement_characteristic_uuid, self.binary_message, response=True)

                    await asyncio.sleep(100.0)                                                                                               #TIME TO STAY ON
                    
                    await client.stop_notify(self.long_payload_characteristic_uuid)
                    await client.disconnect()
        except Exception as e:
            print(f"Exception occurred: {e}")
        print(f"Exiting async loop for address {self.address}")


    def director_func(self):
        asyncio.run(self.establish_streaming())
    


    def client_status(self):
        print(f"Client connection: {self.client.is_connected}")
        return self.client.is_connected
    
    
    
    def _initialize_writer(self):   #if file does not exist, call this
        file_exists = False
        try:
            with open(self.filename, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        self.file = open(self.filename, 'a', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=list(self.encode_custommode1(b'').dtype.names))
        
        if not file_exists:
            self.writer.writeheader()

    def write_row_to_file(self, my_dictionary):
        if self.writer is None:
            self._initialize_writer()

        self.writer.writerow(my_dictionary)
        
        
        
        
if __name__ == "__main__":
    viz.go()
    #env = viz.addChild('Environments/serving_room.osgb')
    avatar = viz.addAvatar('vcc_male2.cfg')
    vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)

    address = "D4:22:CD:00:57:48" # Movella DOT UUID
    body_part = 'Bip01 R UpperArm'
    
    my_limb = Limb(body_part,address,avatar)
