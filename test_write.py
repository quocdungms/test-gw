from bleak import BleakClient
from init import *
# Địa chỉ MAC của module BLE cần giao tiếp
DEVICE_ADDRESS = MAC_ADDRESS
DEVICE_ADDRESS = "C8:70:52:60:9F:38"
# UUID của characteristic hỗ trợ ghi dữ liệu
CHARACTERISTIC_WRITE_UUID = OPERATION_MODE
CHARACTERISTIC_READ_UUID = OPERATION_MODE


async def write_and_verify(CHARACTERISTIC_READ_UUID=None):
    # Dữ liệu cần ghi (ví dụ: đổi mode)
    data_to_write = bytearray([0x00])  # Giá trị 0x03 chỉ là ví dụ

    try:
        # Kết nối đến module
        async with BleakClient(DEVICE_ADDRESS) as client:
            # Kiểm tra kết nối
            if not client.is_connected:
                print("Không thể kết nối với module.")
                return

            print("Đã kết nối với module BLE.")

            # Ghi dữ liệu vào characteristic
            await client.write_gatt_char(CHARACTERISTIC_WRITE_UUID, data_to_write)
            print(f"Dữ liệu {data_to_write} đã được gửi.")

            # Đọc phản hồi (nếu module có phản hồi qua một UUID khác)
            if CHARACTERISTIC_READ_UUID:
                response = await client.read_gatt_char(CHARACTERISTIC_READ_UUID)
                print(f"Phản hồi từ module: {response}")

                # Kiểm tra phản hồi
                if response == data_to_write:
                    print("Dữ liệu đã được ghi thành công và xác nhận.")
                else:
                    print("Ghi dữ liệu không thành công hoặc phản hồi không khớp.")
            else:
                print("Không có UUID để kiểm tra phản hồi.")
    except Exception as e:
        print(f"Lỗi trong quá trình ghi dữ liệu: {e}")


# Chạy hàm async
import asyncio

asyncio.run(write_and_verify())
