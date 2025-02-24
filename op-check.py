import asyncio
from bleak import BleakClient

# UUIDs từ tài liệu
NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"  # Label (GAP service)
OP_MODE_UUID = "3f0afd88-7770-46b0-b5e7-9fc099598964"  # Operation Mode


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

        # Hiển thị dữ liệu thô dưới 3 định dạng
        print("Operation Mode - Dữ liệu thô:")
        print(f"  Byte array: {list(op_mode_data)}")  # Byte array
        print(f"  Hexadecimal: {op_mode_data.hex()}")  # Hex
        print(f"  Bits: {raw_to_bits(op_mode_data)}")  # Bit tách từng byte

        # Giải mã dữ liệu
        op_mode_result = decode_operation_mode(op_mode_data)
        print("Operation Mode (giải mã):")
        if isinstance(op_mode_result, str):
            print(f"  {op_mode_result}")
        else:
            for key, value in op_mode_result.items():
                print(f"  {key}: {value}")



device_address = [ "EB:C3:F1:BC:24:DD", "EB:52:53:F5:D5:90", "E7:E1:0F:DA:2D:82", "D7:7A:01:92:9B:DB", "C8:70:52:60:9F:38"]
# Hàm chính
async def main():
    # Chỉ định địa chỉ thiết bị (thay bằng địa chỉ thực tế của bạn)
    device = "C8:70:52:60:9F:38"  # Ví dụ, thay bằng MAC address thực tế
    await fetch_operation_mode(device)
    # for i in device_address:
    #     await fetch_operation_mode(i)
    #     print("##############################################\n")


if __name__ == "__main__":
    asyncio.run(main())