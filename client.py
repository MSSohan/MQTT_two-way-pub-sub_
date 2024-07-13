import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

# Define MQTT settings
MQTT_USER = ''
MQTT_PASSWORD = ''
MQTT_SERVER = 'broker.emqx.io'
MQTT_PORT = 1883  # Default MQTT port, change if necessary
MQTT_KEEPALIVE = 60  # Keepalive interval in seconds

DEVICE_ID = 'UP12'  # Your device ID

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        topic = f'uprint/kiosk/{DEVICE_ID}'
        client.subscribe(topic, qos=1)
    else:
        print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f'Received message on topic: {msg.topic} with payload: {payload}')

def publish_message(client, topic, payload):
    result = client.publish(topic, payload, qos=1)
    status = result.rc
    if status == mqtt.MQTT_ERR_SUCCESS:
        print(f"Sent `{payload}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

# Create an MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Connect to the MQTT server
client.connect(
    host=MQTT_SERVER,
    port=MQTT_PORT,
    keepalive=MQTT_KEEPALIVE
)

# Start the MQTT client loop
client.loop_start()

# Publish real-time data at 1-second intervals
try:
    while True:
        # Generate real-time data (current timestamp and device ID)
        data = {
            'device_id': DEVICE_ID,
            'status':'Ready',
            'time': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        }
        # Convert data to JSON
        json_data = json.dumps(data)
        topic = 'uprint/kiosk'
        # Publish the JSON data
        publish_message(client, topic, json_data)
        time.sleep(2)
except KeyboardInterrupt:
    print("\nExited by user")

# Stop the loop and disconnect the client
client.loop_stop()
client.disconnect()
