import asyncio
from bleak import BleakScanner, BleakClient
import struct

# UUIDs t? tài li?u
NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"  # Label (GAP service)
LOC_DATA_MODE_UUID = "a02b947e-df97-4516-996a-1882521e0ead"  # Location Data Mode
LOC_DATA_UUID = "003bbdf2-c634-4b3d-ab56-7ec889b89a37"  # Location Data


# Hàm chuy?n d? li?u thô thành chu?i bit
def raw_to_bits(data):
    bit_string = ""
    for byte in data:
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits + " "
    return bit_string.strip()


# Hàm gi?i mã Location Data Mode 2 (Position + Distances)
def decode_location_mode_2(data):
    result = {}

    # Gi?i mã Position (13 bytes d?u tiên)
    x, y, z, quality_pos = struct.unpack("<iiiB", data[:13])
    result["Position"] = {
        "X": x / 1000,  # Chuy?n t? mm sang m
        "Y": y / 1000,
        "Z": z / 1000,
        "Quality Factor": quality_pos
    }

    # Gi?i mã Distances (ph?n còn l?i)
    distances = []
    if len(data) > 13:  # N?u có d? li?u kho?ng cách
        count = data[13]  # S? lu?ng kho?ng cách
        for i in range(count):
            offset = 14 + i * 7
            node_id, distance, quality = struct.unpack("<h i B", data[offset:offset + 7])
            distances.append({
                "Node ID": node_id,
                "Distance": distance / 1000,  # Chuy?n t? mm sang m
                "Quality Factor": quality
            })
        result["Distances"] = distances

    return result


# Hàm l?y d? li?u t? thi?t b?
async def fetch_location_data(address):
    async with BleakClient(address) as client:
        print(f"Ðã k?t n?i t?i {address}")

        # Ð?c tên thi?t b?
        name_data = await client.read_gatt_char(NAME_UUID)
        device_name = name_data.decode("utf-8")
        print(f"Tên thi?t b?: {device_name}")

        # Ð?c Location Data Mode
        loc_mode_data = await client.read_gatt_char(LOC_DATA_MODE_UUID)
        loc_mode = loc_mode_data[0]
        print(f"Location Data Mode: {loc_mode}")

        # Ð?c Location Data
        loc_data = await client.read_gatt_char(LOC_DATA_UUID)
        print(f"D? li?u thô (hex): {loc_data.hex()}")
        print(f"D? li?u thô (bit): {raw_to_bits(loc_data)}")

        # Gi?i mã d? li?u Mode 2 (gi? d?nh mode 2)
        loc_result = decode_location_mode_2(loc_data)
        print("Location Data (Mode 2):")
        for key, value in loc_result.items():
            print(f"  {key}: {value}")


# Quét và k?t n?i t?i thi?t b?
async def main():
    devices = await BleakScanner.discover()
    dwm_device = next((d for d in devices if "DWD40F" in (d.name or "")), None)

    if dwm_device:
        print(f"Tìm th?y thi?t b? DWM: {dwm_device.address}")
        await fetch_location_data(dwm_device.address)
    else:
        print("Không tìm th?y thi?t b? DWM nào")


if __name__ == "__main__":
    asyncio.run(main())