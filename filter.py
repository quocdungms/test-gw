import re

# Ðu?ng d?n t?i file log
log_file_path = "log.txt"

# File d? luu k?t qu?
output_file_path = "module.txt"

# Ð?c n?i dung t? file log
with open(log_file_path, "r", encoding="utf-8") as file:
    log = file.read()

# S? d?ng regex d? trích xu?t các UUID t? "Characteristic"
characteristics = re.findall(r"Characteristic:\s([0-9a-fA-F\-]+)", log)

# Ðua UUID vào m?ng d?ng chu?i
uuid_array = [f'"{uuid}"' for uuid in characteristics]

# Ghi k?t qu? vào file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(", ".join(uuid_array))  # Ghi các UUID thành m?t dòng, cách nhau b?ng d?u ph?y

print(f"K?t qu? dã du?c luu vào file: {output_file_path}")
