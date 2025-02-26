import asyncio
import struct

from bleak import BleakScanner, BleakClient

# UUIDs từ tài liệu
NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"  # Label (GAP service)
LOC_DATA_MODE_UUID = "a02b947e-df97-4516-996a-1882521e0ead"  # Location Data Mode
LOC_DATA_UUID = "003bbdf2-c634-4b3d-ab56-7ec889b89a37"  # Location Data

FILE_NAME = "location_data.txt"

# Hàm ghi dữ liệu vào file TXT
def save_to_txt(device_name, loc_mode, data_size, raw_hex, decoded_data):
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(f"Tên thiết bị: {device_name}\n")
        f.write(f"Location Mode: {loc_mode}\n")
        f.write(f"Số byte nhận: {data_size}\n")
        f.write(f"Dữ liệu thô (hex): {raw_hex}\n")
        f.write(f"Dữ liệu giải mã: {decoded_data}\n")
        f.write("=" * 50 + "\n\n")

# Giải mã Location Data Mode 2
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
    if len(data) > 14:
        count = data[14]  # Số lượng khoảng cách
        result["Count"] = count
        for i in range(count):
            offset = 15 + i * 7
            node_id, distance, quality = struct.unpack("<H i B", data[offset:offset + 7])
            distances.append({
                "Node ID": node_id,
                "Distance": distance / 1000,  # Chuyển từ mm sang m
                "Quality Factor": quality
            })
        result["Distances"] = distances

    return result

# Hàm lấy dữ liệu liên tục mỗi giây
async def fetch_location_data(client):
    name_data = await client.read_gatt_char(NAME_UUID)
    device_name = name_data.decode("utf-8")
    
    loc_mode_data = await client.read_gatt_char(LOC_DATA_MODE_UUID)
    loc_mode = loc_mode_data[0]

    print(f"Đã kết nối: {device_name}, Mode: {loc_mode}")

    while True:
        loc_data = await client.read_gatt_char(LOC_DATA_UUID)
        raw_hex = loc_data.hex()
        decoded_data = decode_location_mode_2(loc_data)

        print(f"Nhận {len(loc_data)} byte từ {device_name}")
        
        # Ghi dữ liệu vào file TXT
        save_to_txt(device_name, loc_mode, len(loc_data), raw_hex, decoded_data)

        await asyncio.sleep(1)  # Đợi 1 giây rồi lấy dữ liệu tiếp

# Quét và kết nối tới thiết bị
async def main():
    devices = await BleakScanner.discover()
    dwm_device = next((d for d in devices if "DWCE07" in (d.name or "")), None)

    if dwm_device:
        async with BleakClient(dwm_device.address) as client:
            await fetch_location_data(client)
    else:
        print("Không tìm thấy thiết bị DWM nào")

if __name__ == "__main__":
    asyncio.run(main())
