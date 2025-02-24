import asyncio
from bleak import BleakScanner, BleakClient
import struct

# UUIDs từ tài liệu
NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"  # Label (GAP service)
OP_MODE_UUID = "3f0afd88-7770-46b0-b5e7-9fc099598964"  # Operation Mode
LOC_DATA_MODE_UUID = "a02b947e-df97-4516-996a-1882521e0ead"  # Location Data Mode
LOC_DATA_UUID = "003bbdf2-c634-4b3d-ab56-7ec889b89a37"  # Location Data


# Hàm chuyển dữ liệu thô thành chuỗi bit
def raw_to_bits(data):
    bit_string = ""
    for byte in data:
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits + " "
    return bit_string.strip()


# Hàm giải mã Operation Mode
def decode_operation_mode(data):
    if len(data) != 2:
        return "Dữ liệu Operation Mode không hợp lệ (cần 2 bytes)"

    byte1, byte2 = data[0], data[1]

    # Byte 1
    node_type = "Tag" if (byte1 & 0x80) == 0 else "Anchor"
    uwb_mode = ["Off", "Passive", "Active"][(byte1 & 0x60) >> 5]
    firmware = "Firmware 1" if (byte1 & 0x10) == 0 else "Firmware 2"
    accel_enable = bool(byte1 & 0x08)
    led_enable = bool(byte1 & 0x04)
    fw_update_enable = bool(byte1 & 0x02)

    # Byte 2
    initiator_enable = bool(byte2 & 0x80)  # Anchor-specific
    low_power_mode = bool(byte2 & 0x40)  # Tag-specific
    loc_engine_enable = bool(byte2 & 0x20)  # Tag-specific

    return {
        "Node Type": node_type,
        "UWB Mode": uwb_mode,
        "Firmware": firmware,
        "Accelerometer Enabled": accel_enable,
        "LED Enabled": led_enable,
        "Firmware Update Enabled": fw_update_enable,
        "Initiator Enabled": initiator_enable,
        "Low Power Mode": low_power_mode,
        "Location Engine Enabled": loc_engine_enable
    }


# Hàm nhận dữ liệu Operation Mode
async def fetch_operation_mode(address):
    async with BleakClient(address) as client:
        print(f"Đã kết nối tới {address}")

        # Đọc tên thiết bị
        name_data = await client.read_gatt_char(NAME_UUID)
        device_name = name_data.decode("utf-8")
        print(f"Tên thiết bị: {device_name}")

        # Đọc Operation Mode
        op_mode_data = await client.read_gatt_char(OP_MODE_UUID)
        print(f"Operation Mode - Dữ liệu thô (hex): {op_mode_data.hex()}")
        print(f"Operation Mode - Dữ liệu thô (bit): {raw_to_bits(op_mode_data)}")

        # Giải mã dữ liệu
        op_mode_result = decode_operation_mode(op_mode_data)
        print("Operation Mode:")
        if isinstance(op_mode_result, str):
            print(f"  {op_mode_result}")
        else:
            for key, value in op_mode_result.items():
                print(f"  {key}: {value}")


# Hàm giải mã Location Data Mode 2 (Position + Distances)
def decode_location_mode_2(data):
    result = {}

    # Giải mã Position (13 bytes đầu tiên)
    x, y, z, quality_pos = struct.unpack("<iiiB", data[:13])
    result["Position"] = {
        "X": x / 1000,  # Chuyển từ mm sang m
        "Y": y / 1000,
        "Z": z / 1000,
        "Quality Factor": quality_pos
    }

    # Giải mã Distances (phần còn lại)
    distances = []
    if len(data) > 13:  # Nếu có dữ liệu khoảng cách
        count = data[13]  # Số lượng khoảng cách
        for i in range(count):
            offset = 14 + i * 7
            node_id, distance, quality = struct.unpack("<h i B", data[offset:offset + 7])
            distances.append({
                "Node ID": node_id,
                "Distance": distance / 1000,  # Chuyển từ mm sang m
                "Quality Factor": quality
            })
        result["Distances"] = distances

    return result


# Hàm nhận dữ liệu Location Data Mode 2
async def fetch_location_data_mode_2(address):
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
        print(f"Location Data - Dữ liệu thô (hex): {loc_data.hex()}")
        print(f"Location Data - Dữ liệu thô (bit): {raw_to_bits(loc_data)}")

        # Giải mã dữ liệu Mode 2
        loc_result = decode_location_mode_2(loc_data)
        print("Location Data (Mode 2):")
        for key, value in loc_result.items():
            print(f"  {key}: {value}")


# Quét và kết nối tới thiết bị
async def main():
    devices = await BleakScanner.discover()
    dwm_device = next((d for d in devices if "DWM" in (d.name or "")), None)

    if dwm_device:
        print(f"Tìm thấy thiết bị DWM: {dwm_device.address}")

        # Test Operation Mode
        print("\n=== Test Operation Mode ===")
        await fetch_operation_mode(dwm_device.address)

        # Test Location Data Mode 2
        print("\n=== Test Location Data Mode 2 ===")
        await fetch_location_data_mode_2(dwm_device.address)
    else:
        print("Không tìm thấy thiết bị DWM nào")


if __name__ == "__main__":
    asyncio.run(main())