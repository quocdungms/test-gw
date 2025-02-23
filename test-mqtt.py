import paho.mqtt.client as mqtt
import json
import time
import random

# Thông tin MQTT broker
MQTT_BROKER = "192.168.1.88"
MQTT_PORT = 1883
MQTT_TOPIC = "gateway/data"
MQTT_CLIENT_ID = "gateway-01"



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối MQTT thành công!")
    else:
        print(f"Kết nối MQTT thất bại với mã lỗi {rc}")



def on_disconnect(client, userdata, rc):
    print("Ngắt kết nối MQTT!")


# Khởi tạo MQTT client
client = mqtt.Client()

# Gán các hàm callback
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Kết nối tới broker
print("Đang kết nối tới MQTT Broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Vòng lặp chính
try:
    client.loop_start()
    while True:

        temperature = round(random.uniform(20.0, 35.0), 1)
        humidity = round(random.uniform(30.0, 80.0), 1)

        data = {
            "device_id": "gateway-01",
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": int(time.time())
        }


        payload = json.dumps(data)


        client.publish(MQTT_TOPIC, payload)
        print(f"Đã gửi dữ liệu: {payload}")


        time.sleep(5)

except KeyboardInterrupt:
    print("Dừng chương trình!")
finally:
    client.loop_stop()
    client.disconnect()
