import asyncio
from bleak import BleakClient
from init import  *
# Địa chỉ MAC của module DWM1001 (Cần quét trước bằng hcitool hoặc bleak)
MODULE_MAC_ADDRESS = "EB:C3:F1:BC:24:DD"

# UUID của dịch vụ và đặc tả cần ghi trên DWM1001
SERVICE_UUID = "0000feee-0000-1000-8000-00805f9b34fb"  # UUID chính của DWM1001
CHAR_UUID_MODE = "0000feef-0000-1000-8000-00805f9b34fb"  # UUID ghi Operation Mode

# Chế độ hoạt động (Operation Mode)
MODE_ANCHOR = b'\x01'  # Anchor Mode
MODE_TAG = b'\x00'  # Tag Mode
location_mode = b'\x00'
async def write_operation_mode(address, mode):
    async with BleakClient(address) as client:
        if await client.is_connected():
            print(f"Đã kết nối với {address}")
            await client.write_gatt_char(LOCATION_DATA_MODE, mode)
            print("Đã ghi chế độ hoạt động thành công!")
        else:
            print("Không thể kết nối với thiết bị.")

# Chọn mode cần ghi (ví dụ: đổi sang Tag mode)
asyncio.run(write_operation_mode(MODULE_MAC_ADDRESS, location_mode))
