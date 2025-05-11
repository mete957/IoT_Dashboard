import os
import time
import random
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTv311

# Ortam değişkenlerinden broker bilgisi alır, yoksa mosquitto’ya bağlanır
BROKER   = os.getenv("MQTT_BROKER", "mosquitto")
PORT     = int(os.getenv("MQTT_PORT", 1883))
TOPIC    = os.getenv("SIM_TOPIC", "test/topic")
INTERVAL = float(os.getenv("SIM_INTERVAL", 5))   # saniye cinsinden aralık

client = mqtt.Client(protocol=MQTTv311)
client.connect(BROKER, PORT)
print(f"[SIM] Connected to {BROKER}:{PORT}, publishing to '{TOPIC}' every {INTERVAL}s")

try:
    while True:
        # 20.00–30.00 arasında rastgele değer
        value = round(random.uniform(20.0, 30.0), 2)
        payload = str(value)
        client.publish(TOPIC, payload)
        print(f"[SIM] Published {payload} to {TOPIC}")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("[SIM] Simulator stopped by user")
