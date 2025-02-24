import asyncio

from Demos.mmapfile_demo import offset
from bleak import BleakScanner, BleakClient
import struct

# UUIDs từ tài liệu
NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"  # Label (GAP service)
LOC_DATA_MODE_UUID = "a02b947e-df97-4516-996a-1882521e0ead"  # Location Data Mode
LOC_DATA_UUID = "003bbdf2-c634-4b3d-ab56-7ec889b89a37"  # Location Data


# Hàm chuyển dữ liệu thô thành chuỗi bit
def raw_to_bits(data):
    bit_string = ""
    for byte in data:
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits + " "
    return bit_string.strip()


# Hàm giải mã Location Data Mode 2 (Position + Distances)
def decode_location_mode_2(data):
    result = {}

    # Giải mã Position (13 bytes đầu tiên)
    x, y, z, quality_pos = struct.unpack("<iiiB", data[1:14])
    result["Position"] = {
        "X": x / 1000,  # Chuyển từ mm sang m
        "Y": y / 1000,
        "Z": z / 1000,
        "Quality Factor": quality_pos
    }

    # Giải mã Distances (phần còn lại)
    distances = []
    if len(data) > 14:  # Nếu có dữ liệu khoảng cách
        count = data[14]  # Số lượng khoảng cách
        for i in range(count):
            offset = 15 + i * 7
            node_id, distance, quality = struct.unpack("<h i B", data[offset:offset + 7])
            distances.append({
                "Node ID": node_id,
                "Distance": distance / 1000,  # Chuyển từ mm sang m
                "Quality Factor": quality
            })
        result["Distances"] = distances

    return result


# Hàm lấy dữ liệu từ thiết bị
async def fetch_location_data(address):
    async with BleakClient(address) as client:
        print(f"Đã kết nối tới {address}")

        # Đọc tên thiết bị
        name_data = await client.read_gatt_char(NAME_UUID)
        device_name = name_data.decode("utf-8")
        print(f"Tên thiết bị: {device_name}")

        # Đọc Location Data Mode
        loc_mode_data = await client.read_gatt_char(LOC_DATA_MODE_UUID)
        loc_mode = loc_mode_data[0]
        print(f"Location Data Mode: {loc_mode}")

        # Đọc Location Data
        loc_data = await client.read_gatt_char(LOC_DATA_UUID)
        print(f"Dữ liệu thô (hex): {loc_data.hex()}")
        print(f"Dữ liệu thô (bit): {raw_to_bits(loc_data)}")

        # Giải mã dữ liệu Mode 2 (giả định mode 2)
        loc_result = decode_location_mode_2(loc_data)
        print("Location Data (Mode 2):")
        for key, value in loc_result.items():
            print(f"  {key}: {value}")


# Quét và kết nối tới thiết bị
async def main():
    devices = await BleakScanner.discover()
    dwm_device = next((d for d in devices if "DWCE07" in (d.name or "")), None)

    if dwm_device:
        print(f"Tìm thấy thiết bị DWM: {dwm_device.address}")
        await fetch_location_data(dwm_device.address)
    else:
        print("Không tìm thấy thiết bị DWM nào")


if __name__ == "__main__":
    asyncio.run(main())