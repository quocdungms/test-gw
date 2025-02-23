import asyncio
from bleak import BleakClient
from docutils.nodes import address

from init import *

DEVICE_ADDRESS = MAC_ADDRESS


client = BleakClient(MAC_ADDRESS)
async def list_uuids():
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected} {DEVICE_ADDRESS}")

        print("Discovering services...")
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} | Properties: {char.properties}")

asyncio.run(list_uuids(DEVICE_ADDRESS))
