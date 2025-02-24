import asyncio
from bleak import BleakClient
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


# Hàm giải mã Location Data Mode 0 (bỏ byte đầu)
def decode_location_mode_0(data):
    if len(data) != 14:
        return f"Dữ liệu không khớp (cần 14 bytes với 1 byte rác, nhận được {len(data)} bytes)"

    # Lấy 13 byte từ byte thứ 2 (index 1) đến cuối
    valid_data = data[1:14]  # Bỏ byte đầu (index 0)
    if len(valid_data) != 13:
        return "Dữ liệu hợp lệ không đủ 13 byte sau khi bỏ byte rác"

    # Giải mã 13 byte: X (4 bytes), Y (4 bytes), Z (4 bytes), Quality (1 byte)
    x, y, z, quality = struct.unpack("<iiiB", valid_data)
    return {
        "Position": {
            "X (mm)": x,  # Giá trị gốc tính bằng mm
            "X (m)": x / 1000,  # Chuyển sang m
            "Y (mm)": y,
            "Y (m)": y / 1000,
            "Z (mm)": z,
            "Z (m)": z / 1000
        },
        "Quality Factor": quality
    }


# Hàm đọc dữ liệu Location Data Mode 0
async def fetch_location_mode_0(address):
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

        # Hiển thị dữ liệu thô dưới 3 định dạng
        print("Location Data - Dữ liệu thô (bao gồm byte rác):")
        print(f"  Byte array: {list(loc_data)}")
        print(f"  Hexadecimal: {loc_data.hex()}")
        print(f"  Bits: {raw_to_bits(loc_data)}")
        print(f"  Độ dài: {len(loc_data)} bytes (14 bytes, byte đầu là rác)")

        # Hiển thị dữ liệu hợp lệ sau khi bỏ byte rác
        valid_data = loc_data[1:14]
        print("Dữ liệu hợp lệ (bỏ byte rác):")
        print(f"  Byte array: {list(valid_data)}")
        print(f"  Hexadecimal: {valid_data.hex()}")
        print(f"  Bits: {raw_to_bits(valid_data)}")

        # Giải mã dữ liệu Mode 0
        loc_result = decode_location_mode_0(loc_data)
        print("Location Data (Mode 0):")
        if isinstance(loc_result, str):
            print(f"  {loc_result}")
        else:
            for key, value in loc_result.items():
                print(f"  {key}:")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"    {value}")


# Hàm chính
async def main():
    # Chỉ định địa chỉ thiết bị (thay bằng địa chỉ thực tế của bạn)
    device_address = "EB:52:53:F5:D5:90"  # Ví dụ, thay bằng MAC address thực tế
    await fetch_location_mode_0(device_address)


if __name__ == "__main__":
    asyncio.run(main())