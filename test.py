from bleak import BleakScanner

async def scan_ble_devices():
    print("Đang quét các thiết bị BLE...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Tên thiết bị: {device.name}, Địa chỉ MAC: {device.address}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(scan_ble_devices())
