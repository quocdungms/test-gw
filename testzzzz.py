import asyncio
from bleak import BleakClient

from init import *
mac = MAC_ADDRESS
addr = LOCATION_DATA_MODE

async def test(mac, uuid):
    async with BleakClient(mac) as client:
        if client.is_connected:
            data = await client.read_gatt_char(uuid)
            print(data)


asyncio.run(test(mac,addr))