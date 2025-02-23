def binary_to_hex(binary_str):
    try:
        # Convert binary string to integer
        decimal_value = int(binary_str, 2)
        # Convert integer to hexadecimal string and remove '0x' prefix
        hex_value = hex(decimal_value)[2:].upper()
        return hex_value
    except ValueError:
        return "Invalid binary string"

# Example usage
binary_string = "0101100100100000"
hex_result = binary_to_hex(binary_string)
print(f"Binary: {binary_string} -> Hex: {hex_result}")
