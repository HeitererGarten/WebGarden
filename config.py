from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import socket

MQTT_BROKER_HOST = "192.168.1.245"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "topic/sensor/#"  # Subscribe to all sensor topics
MQTT_CLIENT_ID = "fastapi_sensor_monitor"

# Database settings
DATABASE_URL = "sqlite:///./db/node_data.db"

# Sensor data polling interval in seconds (2 minutes for testing)
POLLING_INTERVAL = 10  # 2 minutes

# Normal polling interval (for production)
NORMAL_POLLING_INTERVAL = 1800  # 30 minutes
