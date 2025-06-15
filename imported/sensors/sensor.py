import os
import time
import random
import json
import paho.mqtt.client as mqtt

# Sensor configuration from environment
SENSOR_ID = os.getenv('SENSOR_ID', 'sensor_default')
SENSOR_TYPE = os.getenv('SENSOR_TYPE', 'temperature')
MQTT_BROKER = 'mqtt_broker'
MQTT_PORT = 1883
MQTT_TOPIC = f'sensors/{SENSOR_TYPE}/{SENSOR_ID}'

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{SENSOR_ID}] Verbunden mit MQTT Broker")
    else:
        print(f"[{SENSOR_ID}] Verbindung fehlgeschlagen. Code: {rc}")

def on_publish(client, userdata, mid):
    print(f"[{SENSOR_ID}] Nachricht {mid} veröffentlicht")

# Simulate sensor data
def generate_sensor_data():
    if SENSOR_TYPE == 'temperature':
        # Temperature between 18-28°C
        value = round(random.uniform(18.0, 28.0), 2)
    elif SENSOR_TYPE == 'humidity':
        # Humidity between 30-70%
        value = round(random.uniform(30.0, 70.0), 2)
    else:
        value = round(random.random() * 100, 2)
    
    return {
        'sensor_id': SENSOR_ID,
        'type': SENSOR_TYPE,
        'value': value,
        'timestamp': time.time(),
        'unit': '°C' if SENSOR_TYPE == 'temperature' else '%'
    }

# Main program
def main():
    # Create MQTT client
    client = mqtt.Client(client_id=SENSOR_ID)
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    # Connect to broker with retry
    connected = False
    for attempt in range(10):
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            connected = True
            break
        except:
            print(f"[{SENSOR_ID}] Verbindungsversuch {attempt + 1}/10 fehlgeschlagen. Warte 2 Sekunden...")
            time.sleep(2)
    
    if not connected:
        print(f"[{SENSOR_ID}] Konnte keine Verbindung zum MQTT Broker herstellen")
        return
    
    # Start MQTT loop in background
    client.loop_start()
    
    print(f"[{SENSOR_ID}] Sensor gestartet. Sende {SENSOR_TYPE} Daten...")
    
    # Publish sensor data periodically
    while True:
        data = generate_sensor_data()
        payload = json.dumps(data)
        
        result = client.publish(MQTT_TOPIC, payload, qos=1)
        
        # Wait 1-3 seconds between measurements (random for more realistic simulation)
        time.sleep(random.uniform(1.0, 3.0))

if __name__ == "__main__":
    main()