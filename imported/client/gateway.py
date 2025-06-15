import socket
import time
import json
import threading
import paho.mqtt.client as mqtt

# Configuration
HTTP_HOST = 'server'
HTTP_PORT = 8080
MQTT_BROKER = 'mqtt_broker'
MQTT_PORT = 1883
MQTT_TOPICS = [
    ('sensors/+/+', 1),  # Subscribe to all sensor topics with QoS 1
]

# Statistics for performance measurement
message_count = 0
start_time = time.time()
lock = threading.Lock()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[Gateway] Verbunden mit MQTT Broker")
        # Subscribe to topics
        for topic, qos in MQTT_TOPICS:
            client.subscribe(topic, qos)
            print(f"[Gateway] Subscribed to {topic}")
    else:
        print(f"[Gateway] MQTT Verbindung fehlgeschlagen. Code: {rc}")

def on_message(client, userdata, msg):
    global message_count
    
    try:
        # Parse JSON payload
        data = json.loads(msg.payload.decode())
        print(f"[Gateway] Empfangen von {msg.topic}: {data}")
        
        # Format data for HTTP POST
        post_data = f"{data['type']}={data['value']}&sensor={data['sensor_id']}&time={data['timestamp']}"
        
        # Send to HTTP server
        send_http_post(post_data)
        
        # Update statistics
        with lock:
            message_count += 1
            
    except Exception as e:
        print(f"[Gateway] Fehler bei Nachrichtenverarbeitung: {e}")

def send_http_post(data, host=HTTP_HOST, port=HTTP_PORT):
    """Send data via HTTP POST to server"""
    request = f"POST / HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(data)}\r\n\r\n{data}"
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(request.encode())
            response = s.recv(1024)
            print(f"[Gateway] HTTP Response: {response.decode().split()[1]}")
    except Exception as e:
        print(f"[Gateway] HTTP Fehler: {e}")

def print_statistics():
    """Print throughput statistics periodically"""
    global message_count, start_time
    
    while True:
        time.sleep(10)  # Print stats every 10 seconds
        with lock:
            elapsed = time.time() - start_time
            rate = message_count / elapsed * 60  # Messages per minute
            print(f"\n[Gateway Stats] Nachrichten: {message_count} | Rate: {rate:.1f} msg/min\n")

# Main program
def main():
    # Create MQTT client
    client = mqtt.Client(client_id="iot_gateway")
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect to MQTT broker with retry
    connected = False
    for attempt in range(10):
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            connected = True
            break
        except:
            print(f"[Gateway] MQTT Verbindungsversuch {attempt + 1}/10 fehlgeschlagen...")
            time.sleep(2)
    
    if not connected:
        print("[Gateway] Konnte keine Verbindung zum MQTT Broker herstellen")
        return
    
    print("[Gateway] IoT Gateway gestartet")
    
    # Start statistics thread
    stats_thread = threading.Thread(target=print_statistics, daemon=True)
    stats_thread.start()
    
    # Start MQTT loop (blocks forever)
    client.loop_forever()

if __name__ == "__main__":
    main()