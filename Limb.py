from bleak import BleakClient
import viz
import vizcam
import csv
import math
import asyncio
import numpy as np
import vizact
import threading

viz.go()
env = viz.addChild('Environments/serving_room.osgb')
avatar = viz.addAvatar('vcc_male2.cfg')
vizcam.PivotNavigate(center=[0, 1.8, 0], distance=3)

hand = avatar.getBone('Bip01 R UpperArm')
hand.lock()

measurement_characteristic_uuid = '15172001-4947-11e9-8646-d663bd873d93'
short_payload_characteristic_uuid = "15172004-4947-11e9-8646-d663bd873d93"

address = "D4:22:CD:00:57:48" # Movella DOT UUID


def notification_callback(sender, data):
    
    t,w,x,y,z=encode_quaternion(data)[0]
    print(f"Timestamp: {t}, Quaternion-w: {w}")
    quaternion = viz.Quat(w,x,y,z)
    hand.setQuat(quaternion)    
    # hand.setPosition(hand.getPosition()+viz.Vector(x,y,z))

def encode_quaternion(bytes_):
    data_segments = np.dtype([
        ('timestamp', np.uint32),
        ('w', np.float32),
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32)
        ])
    formatted_data = np.frombuffer(bytes_, dtype=data_segments)
    return formatted_data
    
    
client = None

async def establish_streaming():
    global client

    client = BleakClient(address)
    
    if not client.is_connected:
        await client.connect()

    print(f"Client connection: {client.is_connected}") 
    await asyncio.sleep(10)
    if client.is_connected:
        await client.start_notify(short_payload_characteristic_uuid, notification_callback)
        binary_message = b"\x01\x01\x05"  #quaternion mode
        await client.write_gatt_char(measurement_characteristic_uuid, binary_message, response=True)

        await asyncio.sleep(300.0)
        
        await client.stop_notify(short_payload_characteristic_uuid)
        await client.disconnect()
    print("Exiting async loop")



def thread_func():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(establish_streaming())
    finally:
        loop.close()


t = threading.Thread(target=thread_func)
t.start()


#press R to print client status
def client_status():
    global client
    print(f"Client connection: {client.is_connected}")
vizact.onkeydown('r',client_status)