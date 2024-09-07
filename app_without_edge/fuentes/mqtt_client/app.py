import os
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import logging
import time
import re

logging.getLogger().setLevel(logging.INFO)

METADATA_FILE = '/tmp/metadata.json'

def readFile(filename):
    with open('/cfg-data/' + filename) as f:
        data = json.load(f)
        logging.info('File successfully read')
        return data

# Function that is reading json file
data = readFile('env-config.json')
logging.info("Los datos son {}".format(data))
MQTT_BROKER_SERVER = data['env']['MQTT_BROKER_SERVER']
MQTT_USER = data['env']['MQTT_USER']
MQTT_PASSWORD = data['env']['MQTT_PASSWORD']
MQTT_TOPIC_METADATA = data['env']['MQTT_TOPIC_METADATA']
MQTT_TOPIC_DATA = data['env']['MQTT_TOPIC_DATA']
INFLUXDB_IP = data['env']['INFLUXDB_IP']
INFLUXDB_DATABASE = data['env']['INFLUXDB_DATABASE']

metadata_payload = None

def save_metadata(payload):
    global metadata_payload
    for key, value in payload.items():
        if key == 'seq' and value:
            metadata_payload = payload
            logging.info('Metadata is:' + str(metadata_payload))
            with open(METADATA_FILE, 'w') as f:
                json.dump(metadata_payload, f)
            return

def load_metadata():
    global metadata_payload
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata_payload = json.load(f)
            logging.info('Loaded metadata from file: ' + str(metadata_payload))
    else:
        logging.warning('Metadata file does not exist.')

def extract_connection_name(topic):
    try:
        connection_name = re.search('ie/d/j/simatic/v1/s7c1/dp/r/(.+?)/default', topic).group(1)
        logging.info('Connection name is:' + str(connection_name))
        return connection_name
    except AttributeError:
        return None

def extract_names_from_metadata(tag_id, connection_name):
    if not metadata_payload:
        logging.warning('Metadata payload is not available.')
        return None

    tag_name = None
    for key, value in metadata_payload.items():
        if key == 'connections':
            elements = value
            break
    else:
        return None

    for element in elements:
        for key, value in element.items():
            if key == 'name':
                if value == connection_name:
                    continue
                else:
                    break
            if key == 'dataPoints':
                dataPoints = value
                break
        else:
            continue
        break

    for datapoint in dataPoints:
        for key, value in datapoint.items():
            if key == 'dataPointDefinitions':
                definitions = value
                break
        else:
            continue
        break

    for definition in definitions:
        tag_name_found = False
        tag_name = None
        for key, value in definition.items():
            if key == 'id' and value == tag_id:
                tag_name_found = True
            elif key == 'name' and tag_name_found:
                tag_name = value
                return tag_name

    return tag_name

def build_json_influx(dict_values, connection_name):
    logging.info('Datos recibidos para actualizar en la base de datos: ' + str(dict_values))

    # Consultar el último punto en la serie para obtener los valores previos
    previous_values = get_previous_values(connection_name)

    # Actualizar dict_values con los valores previos para los campos que no han cambiado
    for key, value in previous_values.items():
        if key not in dict_values or dict_values[key] is None:
            dict_values[key] = value

    # Filtrar campos con valor None
    dict_values = {key: value for key, value in dict_values.items() if value is not None}

    # Crear el cuerpo JSON para InfluxDB
    json_body = [
        {
            "measurement": connection_name,
            "fields": dict_values
        }
    ]

    logging.info('Datos que se enviarán a InfluxDB: ' + str(json_body))

    # Escribir datos en InfluxDB
    influx_client.write_points(json_body)

def get_previous_values(connection_name):
    # Consulta para obtener el último punto de datos de la serie
    query = f'SELECT * FROM "{connection_name}" ORDER BY time DESC LIMIT 1'
    result = influx_client.query(query)

    if result:
        # Devuelve el último registro si existe
        points = list(result.get_points(measurement=connection_name))
        if points:
            return points[0]  # El último punto de datos
    return {}  # Si no hay puntos previos, devolvemos un diccionario vacío

def extract_data(topic, payload):
    dict_values = dict()
    connection_name = extract_connection_name(topic)
    if connection_name is None:
        logging.warning('Connection name could not be extracted from the topic.')
        return
    
    for key, value in payload.items():
        if key == 'vals':
            vals = value
            break
    else:
        logging.warning('No values found in payload.')
        return

    for tag in vals:
        tag_name = None
        for key, value in tag.items():
            if key == 'id':
                tag_id = value
                tag_name = extract_names_from_metadata(tag_id, connection_name)
            elif key == 'val' and tag_name:
                tag_val = value
                dict_values[tag_name] = tag_val

    logging.info('Data are sending to database is:' + str(dict_values))       
    build_json_influx(dict_values, connection_name)

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_DATA)
    client.subscribe(MQTT_TOPIC_METADATA)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    if msg.topic == MQTT_TOPIC_METADATA:
        save_metadata(payload)
    elif msg.topic == MQTT_TOPIC_DATA:
        extract_data(topic, payload)
    else:
        logging.info('Unknown topic...')

# Llama a load_metadata antes de conectar el cliente MQTT
load_metadata()

time.sleep(5)
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_BROKER_SERVER, 1883, 60)

logging.info('Creating influxdb')

influx_client = InfluxDBClient(INFLUXDB_IP, 8086, "root", "root", INFLUXDB_DATABASE)

# Crear una nueva base de datos y usarla
influx_client.create_database(INFLUXDB_DATABASE)
influx_client.switch_database(INFLUXDB_DATABASE)

# Llamada bloqueante que procesa el tráfico de red, despacha callbacks y maneja reconexiones.
client.loop_forever()
