import os 
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import logging
import time
import re

logging.getLogger().setLevel(logging.INFO)

# Variable global para almacenar metadata
metadata_payload = {}

# Función para leer un archivo JSON
def readFile(filename):
    try:
        with open('/cfg-data/' + filename) as f:
            data = json.load(f)
            logging.info('Archivo leído correctamente')
            return data
    except Exception as e:
        logging.error(f"Error al leer el archivo {filename}: {e}")
        return {}

# Leer configuración
data = readFile('env-config.json')
MQTT_BROKER_SERVER = data['env']['MQTT_BROKER_SERVER']
MQTT_USER = data['env']['MQTT_USER']
MQTT_PASSWORD = data['env']['MQTT_PASSWORD']
MQTT_TOPIC_METADATA = data['env']['MQTT_TOPIC_METADATA']
MQTT_TOPIC_DATA = data['env']['MQTT_TOPIC_DATA']
INFLUXDB_IP = data['env']['INFLUXDB_IP']
INFLUXDB_DATABASE = data['env']['INFLUXDB_DATABASE']

# Función para guardar metadata
def save_metadata(payload):
    global metadata_payload
    if 'seq' in payload and 'connections' in payload:
        metadata_payload = payload
        logging.info('Metadata guardada: ' + str(metadata_payload))
        # Guardar metadata localmente para persistencia
        with open('/cfg-data/metadata_backup.json', 'w') as f:
            json.dump(metadata_payload, f)
            logging.info('Metadata guardada localmente en metadata_backup.json')
    else:
        logging.error('Metadata inválida o incompleta')

# Cargar metadata desde archivo si está disponible
def load_persistent_metadata():
    global metadata_payload
    try:
        with open('/cfg-data/metadata_backup.json') as f:
            metadata_payload = json.load(f)
            logging.info('Metadata cargada desde archivo backup')
    except FileNotFoundError:
        logging.warning('No se encontró archivo de backup de metadata')
    except Exception as e:
        logging.error(f"Error al cargar metadata de archivo: {e}")

# Extraer el nombre de la conexión desde el tópico MQTT
def extract_connection_name(topic):
    try:
        connection_name = re.search('ie/d/j/simatic/v1/s7c1/dp/r/(.+?)/default', topic).group(1)
        logging.info('Nombre de la conexión: ' + connection_name)
        return connection_name
    except AttributeError:
        logging.error('No se pudo extraer el nombre de la conexión')
        return None

# Extraer nombre del tag a partir de su ID usando los metadatos
def extract_names_from_metadata(tag_id, connection_name):
    global metadata_payload
    if not metadata_payload:
        logging.error('No hay metadata disponible')
        return None

    for connection in metadata_payload.get('connections', []):
        if connection.get('name') == connection_name:
            for data_point in connection.get('dataPoints', []):
                for definition in data_point.get('dataPointDefinitions', []):
                    if definition.get('id') == tag_id:
                        return definition.get('name')
    logging.warning(f"No se encontró el tag_name para id: {tag_id} en la conexión {connection_name}")
    return None

# Crear el JSON para InfluxDB y enviarlo
def build_json_influx(dict_values, connection_name):
    if not dict_values:
        logging.error("No hay datos para enviar a InfluxDB")
        return

    json_body = [
        {
            "measurement": connection_name,
            "fields": dict_values
        }
    ]

    try:
        influx_client.write_points(json_body)
        logging.info(f"Datos enviados a InfluxDB: {json_body}")
    except Exception as e:
        logging.error(f"Error al escribir en InfluxDB: {e}, Datos: {json_body}")

# Extraer y procesar los datos del mensaje MQTT
def extract_data(topic, payload):
    connection_name = extract_connection_name(topic)
    if not connection_name:
        return

    dict_values = {}
    for val in payload.get('vals', []):
        tag_id = val.get('id')
        tag_name = extract_names_from_metadata(tag_id, connection_name)
        if tag_name:
            dict_values[tag_name] = val.get('val')
        else:
            logging.warning(f"No se encontró tag_name para id: {tag_id}")

    build_json_influx(dict_values, connection_name)

# Callback cuando se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Conectado al broker MQTT con código de resultado: " + str(rc))
    client.subscribe(MQTT_TOPIC_METADATA)
    client.subscribe(MQTT_TOPIC_DATA)

# Callback cuando se recibe un mensaje MQTT
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    if topic == MQTT_TOPIC_METADATA:
        save_metadata(payload)
    elif topic == MQTT_TOPIC_DATA:
        extract_data(topic, payload)
    else:
        logging.warning("Tópico desconocido: " + topic)

# Inicializar el cliente MQTT e InfluxDB
logging.info('Esperando para levantar los servicios...')
time.sleep(5)

# Cargar metadata persistente si está disponible
load_persistent_metadata()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER_SERVER, 1883, 60)

logging.info('Creando base de datos InfluxDB')

try:
    influx_client = InfluxDBClient(INFLUXDB_IP, 8086, "root", "root", INFLUXDB_DATABASE)
    influx_client.create_database(INFLUXDB_DATABASE)
    influx_client.switch_database(INFLUXDB_DATABASE)
    logging.info('InfluxDB configurado correctamente')
except Exception as e:
    logging.error(f"Error al conectar o configurar InfluxDB: {e}")

# Mantener el loop del cliente MQTT
client.loop_forever()
