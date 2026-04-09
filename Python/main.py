##Fist attempt: Temperature##
# import time
# from arduino.app_utils import *

# print("Hello world!")

# get_temperature = 0 # Your global variable

# def loop():
#     global get_temperature
#     print("prueba")
    
#     # Bridge.call returns the value 'read_sensor' sent back
#     val = Bridge.call("get_temperature")
    
#     if val is not None:
#         get_temperature = val
        
#     print(f"Temperatura en Python: {get_temperature:.2f} °C")
#     time.sleep(1)
#     print("Leyendo temperatura desde Arduino vía Bridge...")
#     time.sleep(10)

# App.run(user_loop=loop)

##Second Attempt: PH test##
# import time
# from arduino.app_utils import *

# print("Iniciando App de Monitoreo...")

# # Global variable for pH
# current_ph = 0.0

# def loop():
#     global current_ph
#     print("--- Nueva Lectura ---")
    
#     # Call the Arduino function
#     result = Bridge.call("get_ph")
    
#     if result is not None:
#         current_ph = result
        
#     print(f"Valor de pH: {current_ph:.2f}")
    
#     time.sleep(1) 
#     print("Sincronizando con sensor de pH...")
#     time.sleep(1) # Adjust delay as needed

# App.run(user_loop=loop)

##Third Attempt: Combined##
# import time
# from arduino.app_utils import *

# print("Iniciando Monitoreo Combinado (Temp + pH)...")

# # Global variables
# current_temp = 0.0
# current_ph = 0.0

# def loop():
#     global current_temp, current_ph
    
#     print("\n--- Consultando Sensores ---")
    
#     # 1. Get Temperature
#     temp_result = Bridge.call("get_temperature")
#     if temp_result is not None:
#         current_temp = temp_result
    
#     # 2. Get pH
#     ph_result = Bridge.call("get_ph")
#     if ph_result is not None:
#         current_ph = ph_result
    
#     # Display Results
#     print(f">> Temperatura: {current_temp:.2f} °C")
#     print(f">> Valor de pH: {current_ph:.2f}")
    
#     # Small delay between loop cycles
#     time.sleep(2)

# # Start the app
# App.run(user_loop=loop)

##Fourth Attempt: With MQTT## 

# import time
# import json
# import random
# import paho.mqtt.client as mqtt
# from arduino.app_utils import *

# #--- MQTT Configuration ---
# MQTT_BROKER = "192.168.31.111" 
# MQTT_PORT = 1883
# MQTT_TOPIC = "arduino/sensors/data"

# # Generate a random ID
# MQTT_CLIENT_ID = f"python-mqtt-{random.randint(0, 1000)}"

# # Setup MQTT Client 
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)

# def on_connect(client, userdata, flags, rc, properties=None):
#     if rc == 0:
#         print(f"Conectado al Broker con ID: {MQTT_CLIENT_ID}")
#     else:
#         print(f"Fallo de conexión. Código: {rc}")

# client.on_connect = on_connect

# # Connect and start background loop
# try:
#     client.connect(MQTT_BROKER, MQTT_PORT, 60)
#     client.loop_start() 
# except Exception as e:
#     print(f"Error de red: {e}")

# 
# current_temp = 0.0
# current_ph = 0.0

# def loop():
#     global current_temp, current_ph # CRITICAL: Ensure these are global
    
#     print("\n--- Intentando lectura del Bridge ---")
    
#     # Bridge calls to Arduino
#     temp_val = Bridge.call("get_temperature")
#     ph_val = Bridge.call("get_ph")
    
#     # Check if we actually got data before updating
#     if temp_val is not None:
#         current_temp = temp_val
#     else:
#         print("Error: No se pudo obtener Temperatura del Bridge")

#     if ph_val is not None:
#         current_ph = ph_val
#     else:
#         print("Error: No se pudo obtener pH del Bridge")
    
#     # Build JSON payload
#     data = {
#         "temp_c": round(current_temp, 2),
#         "ph": round(current_ph, 2)
#     }
    
#     # Publish
#     payload = json.dumps(data)
#     client.publish(MQTT_TOPIC, payload)
    
#     print(f"MQTT Publicado: {payload}")
#     time.sleep(5)

# App.run(user_loop=loop)

##Fifth Attempt: AI detect##

# import time
# import json
# import random
# import paho.mqtt.client as mqtt
# from arduino.app_utils import *
# from arduino.app_bricks.video_objectdetection import VideoObjectDetection

# # --- MQTT Configuration ---
# MQTT_BROKER = "192.168.31.111" 
# MQTT_PORT = 1883
# MQTT_TOPIC = "arduino/sensors/data"
# MQTT_CLIENT_ID = f"python-hydro-{random.randint(0, 1000)}"

# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)

# def on_connect(client, userdata, flags, rc, properties=None):
#     if rc == 0:
#         print(f" Connected to Broker: {MQTT_BROKER}")
#     else:
#         print(f" Connection failed: {rc}")

# client.on_connect = on_connect

# try:
#     client.connect(MQTT_BROKER, MQTT_PORT, 60)
#     client.loop_start() 
# except Exception as e:
#     print(f" Network Error: {e}")

# # --- Global Variables ---
# current_temp = 0.0
# current_ph = 0.0
# axolotl_present = False
# max_confidence = 0.0
# axolotl_counter = 0      
# was_present = False      
# last_detection_time = 0  

# # --- Vision Callback ---
# def on_all_detections(detections: dict):
#     global axolotl_present, max_confidence, axolotl_counter, was_present, last_detection_time
    
#     # Check for "Ajolote"
#     if "Ajolote" in detections and len(detections["Ajolote"]) > 0:
#         axolotl_present = True
#         last_detection_time = time.time() # Update timer
        
#         confidences = [box['confidence'] for box in detections["Ajolote"]]
#         max_confidence = max(confidences)
        
#         if not was_present:
#             axolotl_counter += 1
#             print(f"✨ Axolotl arrival detected! Total: {axolotl_counter}")
        
#         was_present = True
#     else:
#         # This part handles the reset when the brick explicitly sends an empty list
#         axolotl_present = False
#         max_confidence = 0.0
#         was_present = False

# # --- Initialize the CORRECT Brick ---
# # Lowered debounce_sec to 0.1 to allow faster state switching
# video_detector = VideoObjectDetection(None, 0.84, 0.1, False)
# video_detector.on_detect_all(on_all_detections)

# def loop():
#     global current_temp, current_ph, axolotl_present, max_confidence, axolotl_counter, last_detection_time
    
#     # SAFETY RESET: If no detection has been reported for 3 seconds, force False.
#     # This fixes issues where the WebSocket might hang on the last known state.
#     if time.time() - last_detection_time > 3.0:
#         axolotl_present = False
#         max_confidence = 0.0
#         was_present = False

#     # 1. Bridge calls to Arduino
#     temp_val = Bridge.call("get_temperature")
#     ph_val = Bridge.call("get_ph")
    
#     if temp_val is not None:
#         current_temp = temp_val
#     if ph_val is not None:
#         current_ph = ph_val
    
#     # 2. Build combined JSON payload
#     data = {
#         "temp_c": round(current_temp, 2),
#         "ph": round(current_ph, 2),
#         "axolotl_present": axolotl_present,
#         "confidence": round(max_confidence, 2),
#         "total_sightings": axolotl_counter
#     }
    
#     # 3. Publish
#     payload = json.dumps(data)
#     client.publish(MQTT_TOPIC, payload)
    
#     print(f"📡 MQTT: {payload}")
#     time.sleep(2)

# # Start everything
# App.run(user_loop=loop)

##Final Attempt: DB added##

import time
import json
import random
import paho.mqtt.client as mqtt
from arduino.app_utils import *
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from arduino.app_bricks.dbstorage_tsstore import TimeSeriesStore # New Brick

# --- MQTT Configuration ---
MQTT_BROKER = "192.168.31.111" 
MQTT_PORT = 1883
MQTT_TOPIC = "arduino/sensors/data"
MQTT_CLIENT_ID = f"python-hydro-{random.randint(0, 1000)}"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f" Connected to Broker: {MQTT_BROKER}")
    else:
        print(f" Connection failed: {rc}")

client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() 
except Exception as e:
    print(f" Network Error: {e}")

# --- Initialize DB Storage ---
db = TimeSeriesStore()
db.start()

# --- Global Variables ---
current_temp = 0.0
current_ph = 0.0
axolotl_present = False
max_confidence = 0.0
axolotl_counter = 0      
was_present = False      
last_detection_time = 0  

# --- Vision Callback ---
def on_all_detections(detections: dict):
    global axolotl_present, max_confidence, axolotl_counter, was_present, last_detection_time
    
    if "Ajolote" in detections and len(detections["Ajolote"]) > 0:
        axolotl_present = True
        last_detection_time = time.time() 
        
        confidences = [box['confidence'] for box in detections["Ajolote"]]
        max_confidence = max(confidences)
        
        if not was_present:
            axolotl_counter += 1
            print(f"✨ Axolotl arrival detected! Total: {axolotl_counter}")
        
        was_present = True
    else:
        axolotl_present = False
        max_confidence = 0.0
        was_present = False

# --- Initialize Vision Brick ---
video_detector = VideoObjectDetection(None, 0.84, 0.1, False)
video_detector.on_detect_all(on_all_detections)

def loop():
    global current_temp, current_ph, axolotl_present, max_confidence, axolotl_counter, last_detection_time
    
    # SAFETY RESET
    if time.time() - last_detection_time > 3.0:
        axolotl_present = False
        max_confidence = 0.0
        was_present = False

    # 1. Bridge calls to Arduino
    temp_val = Bridge.call("get_temperature")
    ph_val = Bridge.call("get_ph")
    
    if temp_val is not None:
        current_temp = temp_val
    if ph_val is not None:
        current_ph = ph_val
    
    # 2. Log Data to Time Series DB
    # Stores the presence as 1 (True) or 0 (False) for graphing
    db.write_sample("temperature", current_temp)
    db.write_sample("ph_level", current_ph)
    db.write_sample("axolotl_visible", 1 if axolotl_present else 0)
    db.write_sample("total_sightings", axolotl_counter)
    
    # 3. Build combined JSON payload for MQTT
    data = {
        "temp_c": round(current_temp, 2),
        "ph": round(current_ph, 2),
        "axolotl_present": axolotl_present,
        "confidence": round(max_confidence, 2),
        "total_sightings": axolotl_counter
    }
    
    # 4. Publish
    payload = json.dumps(data)
    client.publish(MQTT_TOPIC, payload)
    
    print(f"📡 MQTT & DB: {payload}")
    time.sleep(2)

# Start everything
try:
    App.run(user_loop=loop)
finally:
    # Ensure DB closes properly if the app stops
    db.stop()
