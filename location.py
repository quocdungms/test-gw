import asyncio
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
        # Chuyển mỗi byte thành 8 bit, thêm 0 nếu cần
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits + " "
    return bit_string.strip()


# Hàm giải mã Location Data theo 3 mode
def decode_location_data(data, mode):
    if not data:
        return "Không có dữ liệu vị trí hoặc khoảng cách"

    result = {}

    if mode == 0:  # Mode 0: Position Only
        if len(data) != 13:
            return "Dữ liệu vị trí không hợp lệ (cần 13 bytes)"
        x, y, z, quality = struct.unpack("<iiiB", data)  # Little-endian: 3 int32, 1 uint8
        result = {
            "Position": {
                "X": x / 1000,  # Chuyển từ mm sang m
                "Y": y / 1000,
                "Z": z / 1000
            },
            "Quality Factor": quality
        }

    elif mode == 1:  # Mode 1: Distances Only
        if len(data) < 1:
            return "Dữ liệu khoảng cách không hợp lệ (cần ít nhất 1 byte)"
        count = data[0]  # Số lượng khoảng cách
        if len(data) < 1 + count * 7:  # Mỗi phần tử: NodeID (2 bytes), Distance (4 bytes), Quality (1 byte)
            return f"Dữ liệu khoảng cách không đủ (cần {1 + count * 7} bytes, nhận {len(data)} bytes)"
        distances = []
        for i in range(count):
            offset = 1 + i * 7
            node_id, distance, quality = struct.unpack("<h i B", data[offset:offset + 7])
            distances.append({
                "Node ID": node_id,
                "Distance": distance / 1000,  # Chuyển từ mm sang m
                "Quality Factor": quality
            })
        result = {"Distances": distances}

    elif mode == 2:  # Mode 2: Position + Distances
        if len(data) < 13:
            return "Dữ liệu vị trí và khoảng cách không hợp lệ (cần ít nhất 13 bytes)"
        # Position
        x, y, z, quality_pos = struct.unpack("<iiiB", data[:13])
        result["Position"] = {
            "X": x / 1000,
            "Y": y / 1000,
            "Z": z / 1000,
            "Quality Factor": quality_pos
        }
        # Distances
        if len(data) > 13:
            count = data[13]
            if len(data) < 14 + count * 7:
                return f"Dữ liệu khoảng cách không đủ (cần {14 + count * 7} bytes, nhận {len(data)} bytes)"
            distances = []
            for i in range(count):
                offset = 14 + i * 7
                node_id, distance, quality = struct.unpack("<h i B", data[offset:offset + 7])
                distances.append({
                    "Node ID": node_id,
                    "Distance": distance / 1000,
                    "Quality Factor": quality
                })
            result["Distances"] = distances

    return result


# Hàm lấy dữ liệu từ thiết bị, bao gồm tên và dữ liệu bit
async def fetch_location_data(address):
    async with BleakClient(address) as client:
        print(f"Đã kết nối tới {address}")

        # Đọc tên thiết bị
        name_data = await client.read_gatt_char(NAME_UUID)
        device_name = name_data.decode("utf-8")
        print(f"Tên thiết bị: {device_name}")

        # Đọc Location Data Mode
        loc_mode_data = await client.read_gatt_char(LOC_DATA_MODE_UUID)
        loc_mode = loc_mode_data[0]  # Giá trị: 0, 1, hoặc 2
        print(f"Location Data Mode: {loc_mode}")

        # Đọc Location Data
        loc_data = await client.read_gatt_char(LOC_DATA_UUID)
        print(f"Dữ liệu thô (hex): {loc_data.hex()}")
        print(f"Dữ liệu thô (bit): {raw_to_bits(loc_data)}")

        # Giải mã dữ liệu
        loc_result = decode_location_data(loc_data, loc_mode)
        print("Location Data:")
        if isinstance(loc_result, str):
            print(f"  {loc_result}")
        else:
            for key, value in loc_result.items():
                print(f"  {key}: {value}")


# Quét và kết nối tới thiết bị
async def main():
    devices = await BleakScanner.discover()
    dwm_device = next((d for d in devices if "DWM" in (d.name or "")), None)

    if dwm_device:
        print(f"Tìm thấy thiết bị DWM: {dwm_device.address}")
        await fetch_location_data(dwm_device.address)
    else:
        print("Không tìm thấy thiết bị DWM nào")


if __name__ == "__main__":
    asyncio.run(main())