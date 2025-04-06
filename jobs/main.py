from datetime import datetime, timedelta
import os
import uuid
from confluent_kafka import SerializingProducer
import simplejson as json
import random

LONDON_COORDINATES = { "latitude": 51.5074, "longitude": -0.1278 }
BERMINGHAM_COORDINATES = { "latitude": 52.4862, "longitude": -1.8904 }

# Calculate movement of increments
LATITUDE_INCREMENT = (BERMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BERMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100

# Enviroment Variable for configuration
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vechicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')


start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()


def get_next_time():
    global start_time

    start_time += timedelta(seconds=random.randint(30, 60)) # update frequency
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceId':device_id,
        'timestamp' : timestamp,
        'speed': random.uniform(0, 40), # km/h        
        'direction' : 'North-East',
        'vehicleType' : vehicle_type
    }

def generate_traffic_camera_data(device_id, timestamp, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId' : device_id,
        'cameraId' : camera_id,
        'timestamp' : timestamp,
        'snapshot' : 'Base64EncodedString'
    }

def simulate_vehcle_movement():
    global start_location

    # move towards bermingham
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    # add some randomness to simulate acutal road travel
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] +=  random.uniform(-0.0005, 0.0005)

    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehcle_movement()

    return {
        "id": uuid.uuid4(),
        "deviceId" : device_id,
        "timestamp" : get_next_time().isoformat(),
        "location": (location['latitude'], location['longitude']),
        "speed" : random.uniform(10, 40),
        "direction" : "North-East",
        "make": random.choice(["BMW","Audi", "Tesla", "TATA"]),
        "model" : random.choice(["C500", "C100", "C200", "C300"]),
        "year" : 2025,
        "fullType": "Hybrid"
    }

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(device_id,  vehicle_data['timestamp'], 'Nikon-Cam123')
        break

if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'error_cb': lambda e: print(f"Kakfa error: {e}")
    }

    producer = SerializingProducer(producer_config)

    try:
        simulate_journey(producer, 'vehicle-nf-123')

    except KeyboardInterrupt:
        print("Simulation ended by user")
    except Exception as e:
        print(f"Unexpected error occured: {e}")