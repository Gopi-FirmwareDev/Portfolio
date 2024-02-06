import paho.mqtt.client as mqtt
import time

# MQTT broker address and port
broker_address = "localhost"
broker_port = 1883

# Callback function for when the subscribing client connects to the broker
def on_connect_subscribe(client, userdata, flags, rc):
    # Subscribe to a topic upon successful connection
    client.subscribe("channel1")

# Callback function for when a message is received on a subscribed topic
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload.decode("utf-8")) + "' on topic '" + message.topic + "'")

# Create an MQTT client instance for publishing
publish_client = mqtt.Client()

# Connect to the MQTT broker for publishing
publish_client.connect(broker_address, broker_port, 60)

# Create an MQTT client instance for subscribing
subscribe_client = mqtt.Client()

# Set the callback functions for the subscribing client
subscribe_client.on_connect = on_connect_subscribe
subscribe_client.on_message = on_message

# Connect to the MQTT broker for subscribing
subscribe_client.connect(broker_address, broker_port, 60)

# Start the MQTT subscribing client loop to handle network communication and callbacks
subscribe_client.loop_start()

# Publish a message every 5 seconds
while True:
    publish_client.publish("channel1", "Hello, subscriber from publisher!")
    time.sleep(5)
