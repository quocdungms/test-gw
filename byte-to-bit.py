import asyncio

from bleak import BleakClient

from init import *
# from init import MAC_ADDRESS
from uuid_define import *


DEVICE_ADDRESS = MAC_ADDRESS

# UUID = OPERATION_MODE
# UUID = LOCATION_DATA_MODE
UUID = LOCATION_DATA


def read_and_decode_bits(address, uuid):
    async def read_ble():
        async with BleakClient(address) as client:
            if client.is_connected:
                print("Connected to device!")
                print(f"MAC ADDRESS: {DEVICE_ADDRESS}")
                print(f"UUID: {UUID}")
                raw_data = await client.read_gatt_char(uuid)
                print(f"Raw data (bytearray): {raw_data}")
                print(f"Hex: {raw_data.hex()}")
                # for i, byte in enumerate(raw_data):
                #     print(f"Byte {i + 1}: {hex(byte)} ; Demical: {byte}")

                data = decode_byte_to_bits(raw_data)
                print(f"Bit: {data}")





                # data_write = '00000000'
                # data_write = bits_to_bytearray(data_write)
                # print(data_write)
                #
                # await client.write_gatt_char(UUID, data_write)


                bc = count_bytes(data)
                print(f"Bytes count: {bc}")


                # bit = '0101100100100000'
                # data_write = bits_to_bytearray(bit)
                # print(f"Data: {bit}")
                # print(f"Convert to byte array: {data_write}")
                # await client.write_gatt_char(UUID, data_write)
                # print(f"Write {data_write} to UUID: {UUID}")
                # print(f"Rescan Operation mod...")
                # raw_data = await  client.read_gatt_char(UUID)
                # print(f"Raw data (bytearray): {raw_data}")
                # data = decode_byte_to_bits(raw_data)
                # print(f"Bit: {data}")
                # bc = count_bytes(data)
                # print(f"Bytes count: {bc}")
                # # await client.write_gatt_char(UUID, data_write)




    asyncio.run(read_ble())


def decode_byte_to_bits(byte_data):
    return ' '.join(format(byte, '08b') for byte in byte_data)


def encode_bits_to_byte_array(bit_data):
    if len(bit_data) % 8 != 0:
        raise ValueError("Độ dài chuỗi bit phải chia hết cho 8.")
    bytes(int(bit_data[i:i + 8], 2) for i in range(0, len(bit_data), 8))
    return bytes(int(byte, 2) for byte in bit_data)

def to_binary_list(binary_data):
    return binary_data
def list_to_binary(binary_list):
    return ''.join(binary_list)
def count_bytes(data):
    cleaned_data = data.replace(" ", "")
    if len(cleaned_data) % 8 != 0:
        raise ValueError("Invalid data length; must be a multiple of 8 bits.")
    num_bytes = len(cleaned_data) // 8
    return num_bytes


def binary_to_decimal(binary_str):
    decimal = int(binary_str, 2)
    return decimal


def bits_to_bytearray(bit_string):
    """
    Chuyển đổi một chuỗi bit thành một byte array.

    :param bit_string: Chuỗi bit (chuỗi các ký tự '0' và '1')
    :return: Một byte array
    """
    # Kiểm tra nếu độ dài chuỗi không phải bội số của 8
    if len(bit_string) % 8 != 0:
        raise ValueError("Chuỗi bit phải có độ dài là bội số của 8.")

    # Chuyển chuỗi bit thành byte array
    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    return byte_array
# Gọi hàm
# read_and_decode_bits(DEVICE_ADDRESS, UUID)
print(encode_bits_to_byte_array("00000000"))

