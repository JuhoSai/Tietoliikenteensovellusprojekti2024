import mysql.connector
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

# Configuration
ADDRESS = "CF:01:6D:B4:C3:83"
MODEL_NBR_UUID = "00001526-1212-efde-1523-785feabcd123"
DB_CONFIG = {
    "host": "172.20.241.9",
    "user": "dbaccess_rw",
    "password": "fasdjkf2389vw2c3k234vk2f3",
    "database": "measurements"
}

# Sensor data state
sensor_data = {"x": 0, "y": 0, "z": 0, "dir": 0}
sensor_count = 0
# MySQL Insert Function
def mysql_send(sensor_data):
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        mycursor = mydb.cursor()
        sql = (
            "INSERT INTO rawdata(groupid, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_f) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        val = ('212', sensor_data["x"], sensor_data["y"], sensor_data["z"], sensor_data["dir"])
        mycursor.execute(sql, val)
        mydb.commit()
        print("Data inserted into MySQL:", sensor_data)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Bluetooth Notification Callback
def callback(sender: BleakGATTCharacteristic, data: bytearray):
    byte_data = bytes(data)
    global sensor_count
    if len(byte_data) >= 2:
        sensor_value = int.from_bytes(byte_data[:2], byteorder="little")
        print(f"Received sensor_value: {sensor_value}")
        print("sensor_count: ", sensor_count)
        if sensor_count == 0 and sensor_value >= 6:
            return
            print("sensor0 value too large")
        if sensor_count == 0 and sensor_value <= 5:
            sensor_data["dir"] = sensor_value
            print(f"Direction: {sensor_value}")
        elif sensor_count == 1 and sensor_value >= 6:
            sensor_data["x"] = sensor_value
            print(f"X-Axis: {sensor_value}")
        elif sensor_count == 2 and sensor_value >= 6:
            sensor_data["y"] = sensor_value
            print(f"Y-Axis: {sensor_value}")
        elif sensor_count == 3 and sensor_value >= 6:
            sensor_data["z"] = sensor_value
            print(f"Z-Axis: {sensor_value}")

        sensor_count += 1

        if sensor_count == 4:
            mysql_send(sensor_data)
            sensor_data.update({"x": 0, "y": 0, "z": 0, "dir": 0})
            sensor_count = 0

# Notify Function
async def notify():
#    device = await BleakScanner.find_device_by_name("Ryhma12")
#    if not device:
#        print("Device not found")
#        return
    global sensor_count
    sensor_count = 0
    async with BleakClient(ADDRESS) as client:
        await client.start_notify(MODEL_NBR_UUID, callback)
        print("Started notification. Collecting data for 10 seconds...")
        await asyncio.sleep(30)  # Keep the connection open for 10 seconds
        print("Stopping notification.")
        await client.stop_notify(MODEL_NBR_UUID)

# Main Function
async def main():
    try:
        await notify()
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        print("Program completed. Exiting.")

# Run the program
if __name__ == "__main__":
    asyncio.run(main())

