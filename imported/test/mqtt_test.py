import time
import statistics
import subprocess
import docker
import threading

# Test configuration
TEST_DURATION = 60  # seconds
SENSOR_COUNT = 5    # number of sensors to spawn

def collect_gateway_stats(client, duration):
    """Collect message throughput from gateway logs"""
    gateway_container = client.containers.get('gateway')
    
    message_counts = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        logs = gateway_container.logs(tail=50).decode()
        
        # Extract rate from logs
        for line in logs.split('\n'):
            if 'Rate:' in line:
                try:
                    rate = float(line.split('Rate:')[1].split('msg/min')[0].strip())
                    message_counts.append(rate)
                except:
                    pass
        
        time.sleep(5)
    
    return message_counts

def run_mqtt_test():
    print(f"=== MQTT Performance Test ===")
    print(f"Dauer: {TEST_DURATION}s | Sensoren: {SENSOR_COUNT}")
    
    # Docker client
    client = docker.from_env()
    
    # Start infrastructure
    print("\nStarte Infrastruktur...")
    subprocess.run(["docker-compose", "up", "-d", "mqtt_broker", "server", "rpc_db", "gateway"])
    time.sleep(5)  # Wait for services to start
    
    # Start sensors
    print(f"\nStarte {SENSOR_COUNT} Sensoren...")
    for i in range(SENSOR_COUNT):
        subprocess.run([
            "docker-compose", "run", "-d", "--name", f"sensor_test_{i}",
            "-e", f"SENSOR_ID=sensor_test_{i}",
            "-e", f"SENSOR_TYPE={'temperature' if i % 2 == 0 else 'humidity'}",
            "sensor1"
        ])
        time.sleep(0.5)
    
    # Collect statistics
    print("\nSammle Statistiken...")
    rates = collect_gateway_stats(client, TEST_DURATION)
    
    # Cleanup
    print("\nRäume auf...")
    for i in range(SENSOR_COUNT):
        try:
            container = client.containers.get(f"sensor_test_{i}")
            container.stop()
            container.remove()
        except:
            pass
    
    # Calculate results
    if rates:
        print("\n=== Ergebnisse ===")
        print(f"Durchschnittlicher Durchsatz: {statistics.mean(rates):.1f} msg/min")
        print(f"Min: {min(rates):.1f} msg/min")
        print(f"Max: {max(rates):.1f} msg/min")
        print(f"StdDev: {statistics.stdev(rates):.1f} msg/min" if len(rates) > 1 else "StdDev: N/A")
        print(f"Messungen: {len(rates)}")
    else:
        print("Keine Daten gesammelt!")

if __name__ == "__main__":
    run_mqtt_test()