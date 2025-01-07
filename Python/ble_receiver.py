

import mysql.connector
import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

sensor_dir = 0
sensor_x = 0
sensor_y = 0
sensor_z = 0
sensor_count = 0
address = "EF:8C:36:57:C3:7E"
MODEL_NBR_UUID = "00001526-1212-efde-1523-785feabcd123"
mydb = mysql.connector.connect(host="172.20.241.9",user="dbaccess_rw",password="fasdjkf2389vw2c3k234vk2f3",database="measurements")
mycursor = mydb.cursor()



def mysql_send(sensor_x,sensor_y,sensor_z,sensor_dir):

    sql = "INSERT INTO rawdata(groupid, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_f) VALUES (%s, %s, %s, %s, %s)"
    val = ('999', sensor_x, sensor_y, sensor_z, sensor_dir)
    mycursor.execute(sql,val)
    mydb.commit()



def callback(sender: BleakGATTCharacteristic, data: bytearray):
# read incoming data to byte_data
    byte_data = bytes(data)
    global sensor_dir
    global sensor_x
    global sensor_y
    global sensor_z
    global sensor_count

    if len(byte_data) >= 2:
        sensor_value = int.from_bytes(byte_data[:2], byteorder='little')
        if(sensor_count == 4):
            sensor_count = 0

        if(sensor_count == 0):
            sensor_dir = sensor_value
        if(sensor_count == 1):
            sensor_x = sensor_value
        if(sensor_count == 2):
            sensor_y = sensor_value
        if(sensor_count == 3):
            sensor_z = sensor_value
        sensor_count = sensor_count + 1



'''
    #convert data to an integer, if bytearray contains a value
    if len(byte_data) >= 2:
        sensor_value = int.from_bytes(byte_data[:2], byteorder='little')
        sensor_dir = sensor_value
        print("sensor: ",sensor_value)
        if(sensor_y < 0):
            sensor_z = sensor_value
        if(sensor_x < 0):
            sensor_y = sensor_value
        if(sensor_x == 0):
            sensor_x = sensor_value
'''

async def notify():
    global sensor_dir
    global sensor_x
    global sensor_y
    global sensor_z
    global sesnor_count

    device = await BleakScanner.find_device_by_name("R12")
    if not device:
        print("Device not found")
        return

    async with BleakClient(address) as client:
        await client.start_notify(MODEL_NBR_UUID, callback)

    if(sensor_count == 4):
        mysql_send(sensor_x,sensor_y,sensor_z,sensor_dir)
        print(sensor_dir)
        print(sensor_x)
        print(sensor_y)
        print(sensor_z)

        sensor_dir = 0
        sensor_x = 0
        sensor_y = 0
        sensor_z = 0


async def main(address):
    while True:
        await notify()
        await asyncio.sleep(1)



asyncio.run(main(address))
