import time
import threading
import subprocess
import statistics
from concurrent.futures import ThreadPoolExecutor

def test_http_rtt():
    """Test HTTP RTT while system is under load"""
    rtts = []
    for _ in range(100):
        start = time.time()
        subprocess.run(
            ["docker-compose", "run", "--rm", "client"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        rtts.append(time.time() - start)
        time.sleep(0.1)
    return rtts

def test_rpc_response():
    """Test RPC response time while system is under load"""
    # Run your existing RPC test
    result = subprocess.run(
        ["docker-compose", "exec", "server", "python", "rpc_test.py"],
        capture_output=True,
        text=True
    )
    # Parse results from output
    return result.stdout

def run_combined_test():
    print("=== Combined Load Test ===")
    print("Teste alle Schnittstellen unter MQTT-Last...\n")
    
    # Start all services including multiple sensors
    subprocess.run(["docker-compose", "up", "-d"])
    time.sleep(5)
    
    # Run tests in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        http_future = executor.submit(test_http_rtt)
        
        # Get results
        http_rtts = http_future.result()
        
    # Print results
    print("\nHTTP RTT unter MQTT-Last:")
    print(f"Durchschnitt: {statistics.mean(http_rtts):.5f}s")
    print(f"Min: {min(http_rtts):.5f}s | Max: {max(http_rtts):.5f}s")

if __name__ == "__main__":
    run_combined_test()