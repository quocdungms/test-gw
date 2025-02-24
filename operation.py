import asyncio
from bleak import BleakClient
from init import *
# Địa chỉ MAC hoặc UUID của thiết bị BLE
DEVICE_ADDRESS = MAC_ADDRESS # Thay thế bằng địa chỉ thiết bị của bạn
CHARACTERISTIC_UUID = OPERATION_MODE  # UUID của characteristic
CHARACTERISTIC_UUID = LOCATION_DATA_MODE # UUID của characteristic
async def write_ble_data():
    try:
        # Kết nối đến thiết bị BLE
        async with BleakClient(DEVICE_ADDRESS) as client:
            # Kiểm tra xem thiết bị có kết nối thành công không
            if await client.is_connected():
                print(f"Connected: {MAC_ADDRESS}")
                raw_data = client.read_gatt_char(CHARACTERISTIC_UUID)

                # Dữ liệu cần ghi (byte array)
                data = bytearray([0x01, 0x02, 0x03])  # Thay đổi dữ liệu theo yêu cầu

                # Ghi dữ liệu lên characteristic
                await client.write_gatt_char(CHARACTERISTIC_UUID, data)
                print("Đã ghi dữ liệu thành công!")

            else:
                print("Không thể kết nối với thiết bị.")
    except Exception as e:
        print(f"Lỗi: {e}")

# Chạy chương trình
asyncio.run(write_ble_data())
