import os
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# MQTT ayarları
BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT   = int(os.getenv("MQTT_PORT", 1883))

# InfluxDB ayarları
INFLUX_URL    = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN", "admin123")
INFLUX_ORG    = os.getenv("INFLUX_ORG", "my_org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "iot_data")

# InfluxDB client ve write API
client_db = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_db.write_api(write_options=SYNCHRONOUS)

# MQTT client'ı Callback API v2 ile oluşturma (varsa)
if hasattr(mqtt, "CallbackAPIVersion"):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
else:
    client = mqtt.Client()

# Bağlanma callback (v2 signature içerir)
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code", rc, flush=True)
    client.subscribe("test/topic")

# Mesaj alındığında çalışacak fonksiyon
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"{msg.topic} -> {payload}", flush=True)
    try:
        point = (
            Point("measurement1")
            .tag("topic", msg.topic)
            .field("value", float(payload))
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("Written to InfluxDB", flush=True)
    except Exception as e:
        print("Error writing to InfluxDB:", e, flush=True)

# Callback'leri ata
client.on_connect = on_connect
client.on_message = on_message

# Broker'a bağlan ve döngüye gir
print(f"Connecting to MQTT broker at {BROKER}:{PORT}", flush=True)
client.connect(BROKER, PORT)
client.loop_forever()
