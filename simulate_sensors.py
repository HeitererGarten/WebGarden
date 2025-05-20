"""
Test script to simulate sending MQTT messages with sensor data
This will help you test your system without actual sensors
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT
import os


RESTART_FLAG = False  # Set this flag to True to trigger a database reset

def reset_database_if_needed():
    global RESTART_FLAG
    db_path = "db/sensor_data.db"
    if RESTART_FLAG:
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
                print("Database reset: sensor_data.db deleted.")
            else:
                print("Database reset: sensor_data.db does not exist.")
        except Exception as e:
            print(f"Error deleting database: {e}")
        finally:
            RESTART_FLAG = False



# MQTT Configuration
MQTT_TOPIC_PREFIX = "topic/sensor"
MQTT_CLIENT_ID = "sensor_simulator"

# Sensor Configuration
HUB_COUNT = 2
SENSORS_PER_HUB = 3
PUBLISH_INTERVAL = 30  # seconds

def generate_sensor_data(hub_id, sensor_id):
    """Generate random sensor data"""
    now = datetime.now()
    
    return {
        "sensor_id": f"S-{sensor_id}",
        "hub_id": f"H-{hub_id}",
        "temp": round(random.uniform(15.0, 35.0), 1),
        "humidity": round(random.uniform(30.0, 90.0), 1),
        "moisture": round(random.uniform(20.0, 80.0), 1),
        "date": {
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second
        }
    }

def on_connect(client, userdata, flags, rc):
    """Callback for MQTT connection"""
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")

def main():
    reset_database_if_needed()
    # Create MQTT client
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    
    try:
        # Connect to broker
        print(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        client.loop_start()
        
        # Main loop to publish data
        print(f"Publishing sensor data every {PUBLISH_INTERVAL} seconds. Press Ctrl+C to stop.")
        iteration = 0
        
        while True:
            iteration += 1
            print(f"\nIteration {iteration}")
            
            # Publish data for each sensor
            for hub_id in range(HUB_COUNT):
                for sensor_id in range(SENSORS_PER_HUB):
                    # Generate data
                    data = generate_sensor_data(hub_id, sensor_id)
                    
                    # Create topic (sensors/HUB_ID/SENSOR_ID)
                    topic = f"{MQTT_TOPIC_PREFIX}/{data['hub_id']}/{data['sensor_id']}"
                    
                    # Publish
                    payload = json.dumps(data)
                    client.publish(topic, payload)
                    print(f"Published to {topic}: {payload}")
            
            # Wait for next iteration
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nStopping sensor simulator...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    
    main()

