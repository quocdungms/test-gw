def decodeByteToBit(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)


def bits_to_bytearray(bit_string):
    if len(bit_string) % 8 != 0:
        raise ValueError("Chuỗi bit phải có độ dài là bội số của 8.")
    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    return byte_array
# data = '0101100101100000'
data = '1101100110100000'
print(bits_to_bytearray(data))