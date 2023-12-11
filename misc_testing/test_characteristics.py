
from bleak import BleakClient
import viz
import math
import asyncio
import numpy as np

import csv
from datetime import datetime



address = "D4:22:CD:00:57:48"

measurement_characteristic_uuid = "15172001-4947-11e9-8646-d663bd873d93"
long_payload_characteristic_uuid = "15172002-4947-11e9-8646-d663bd873d93"
medium_payload_characteristic_uuid = "15172003-4947-11e9-8646-d663bd873d93"
short_payload_characteristic_uuid = "15172004-4947-11e9-8646-d663bd873d93"


def time_string():
	return "[" + datetime.now().strftime("%H:%S") + "]"

	
async def get_status_v2(client):
	if(client == None):
		print(time_string(), "No client connected")
		return
	message = await client.read_gatt_char(measurement_characteristic_uuid)
	#message = b"\x01\x01\x1a"
	parse_gatt_message(message)
	
def parse_gatt_message(data):
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
	
async def establish_connection(address):
	try:
		client = BleakClient(address)
		print(f"Connection status for client {address}: {client.is_connected}") 
		await asyncio.sleep(1)
		if client.is_connected:
			control_message = b"\x01\x00\x01"
			await client.write_gatt_char(measurement_characteristic_uuid, control_message, response=True)
			await get_status_v2(client)
			return client


	except Exception as e:
		print(f"ESTABLISH STREAMING---Exception occurred: {e}")


long_payload_characteristics = {
    25: "Custom mode 4",
    26: "Custom mode 5"
}

	
medium_payload_characteristics = {
    2: "Extended (Quaternion)",
    3: "Complete (Quaternion)",
    7: "Extended (Euler)",
    16: "Complete (Euler)",
    1: "High Fidelity (with mag)",
    17: "High Fidelity",
    18: "Delta quantities (with mag)",
    19: "Delta quantities",
    20: "Rate quantities (with mag)",
    21: "Rate quantities",
    22: "Custom mode 1",
    23: "Custom mode 2",
    24: "Custom mode 3"
}
	
short_payload_characteristics = {
    4: "Orientation (Euler)",
    5: "Orientation (Quaternion)",
    6: "Free Acceleration",

}

streaming_flag = False
num_bytes = 0
def notification_handler(data):
	streaming_flag = True
	num_bytes = len(data)
	pass
	
	
async def test_streaming(client, characteristic_uuid, mode):
	binary_message = b"\x01\x01" + mode.to_bytes(1, 'big')
	#parse_gatt_message(binary_message)
	if(client == None):
		print(time_string(), "No client connected")
		return
	
	await client.start_notify(characteristic_uuid,notification_handler)
	await client.write_gatt_char(measurement_characteristic_uuid, binary_message, response=True)

	await asyncio.sleep(2)
	await get_status_v2(client)
	await asyncio.sleep(2)

	stop_message = b"\x01\x00\x01"
	await client.write_gatt_char(measurement_characteristic_uuid, stop_message, response = True)
	await client.stop_notify(characteristic_uuid)
	

async def test_dic_codes(client,uuid,dictionary):
	for code, name in dictionary.items():
		streaming_flag = False
		num_bytes = 0
		
		await test_streaming(client,uuid,code)
	
		await get_status_v2(client)
		success_or_not = "Success" if streaming_flag else "Failure"
		print(time_string(), f"Streaming: {success_or_not}, Bytes: {num_bytes}")
		await asyncio.sleep(0.4)
	
	
	
	
async def main_loop():

	client = await establish_connection(address)
	
	
	#short payload
	await test_dic_codes(client,short_payload_characteristic_uuid,short_payload_characteristics)
	
	await test_dic_codes(client,medium_payload_characteristic_uuid, medium_payload_characteristics)
	
	await test_dic_codes(client,long_payload_characteristic_uuid, long_payload_characteristics)
		

		
stop_message = b"\x01\x00\x01"
print(stop_message)		
		
asyncio.run(main_loop())