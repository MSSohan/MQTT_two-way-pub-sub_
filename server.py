import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import json

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app for MQTT settings
app.config['MQTT_USER'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_SERVER'] = 'broker.emqx.io'
app.config['MQTT_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60

# Callback function when the client connects to the broker
def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        topic = 'uprint/kiosk'
        mqtt_client.subscribe(topic, qos=1)
    else:
        print('Bad connection. Code:', rc)

# Callback function when a message is received
def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        device_id = data['device_id']
        response_topic = f'uprint/kiosk/{device_id}'
        response_message = json.dumps({'response': 'Message received', 'device_id': device_id})
        mqtt_client.publish(response_topic, response_message, qos=1)
        print(f"Sent return response '{response_message}' to `{response_topic}`")
    except (json.JSONDecodeError, KeyError):
        print("Invalid message format")

# Function to publish a message
def publish_message(mqtt_client, topic, payload):
    result = mqtt_client.publish(topic, payload, qos=1)
    status = result.rc
    if status == 0:
        print(f"Sent `{payload}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

# Create an MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(app.config['MQTT_USER'], app.config['MQTT_PASSWORD'])

# Connect to the MQTT server
client.connect(
    host=app.config['MQTT_SERVER'],
    port=app.config['MQTT_PORT'],
    keepalive=app.config['MQTT_KEEPALIVE']
)

# Start the MQTT client loop in a separate thread
client.loop_start()

@app.route('/')
def index():
    return jsonify({'message': 'Flask app is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
