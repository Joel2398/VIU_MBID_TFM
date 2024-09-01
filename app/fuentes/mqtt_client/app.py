import os 
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import logging
import time
import re 

logging.getLogger().setLevel(logging.INFO)


def readFile(filename):
    with open('/cfg-data/'+filename) as f:
        data = json.load(f)
        logging.info('File succesfully read')
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

def save_metadata(payload):
    ###We need to keep metadata payload to be able to extract tag names comparing the ids we receive wiht the data payload
    # Para entender esto ver Doc OPC-UA Connector IE en el capitulo 8.4.1 y 8.4.2
    global metadata_payload
    for key,value in payload.items():
        if (key == 'seq'):
            if (value):
                metadata_payload = payload
                logging.info('Metadata is:' + str(metadata_payload))
                exit
        

def extract_connection_name(topic):
    try:
        connection_name = re.search('ie/d/j/simatic/v1/s7c1/dp/r/(.+?)/default', topic).group(1)
        logging.info('Connection name is:' + str(connection_name))
        return connection_name
    except AttributeError:
        pass

def extract_names_from_metadata(tag_id, connection_name):
    # Inicializa la variable tag_name al principio
    tag_name = None

    # Función para extraer el nombre del tag a partir de su ID en los metadatos
    for key, value in metadata_payload.items():
        if key == 'connections':
            elements = value  # Almacena las conexiones
            break  # Usa break en lugar de exit para salir del bucle

    for element in elements:
        for key, value in element.items():
            if key == 'name':
                if value == connection_name:
                    continue  # Sigue al siguiente bloque si hay coincidencia
                else:
                    break  # Sal del bucle si no hay coincidencia

            if key == 'dataPoints':
                dataPoints = value  # Almacena los puntos de datos
                break  # Usa break para salir del bucle

    for datapoint in dataPoints:
        for key, value in datapoint.items():
            if key == 'dataPointDefinitions':
                definitions = value  # Almacena las definiciones de puntos de datos
                break  # Usa break para salir del bucle

    for definition in definitions:
        # Reorganiza las condiciones para asignar tag_name correctamente
        tag_name_found = False  # Bandera para indicar si se encuentra el nombre del tag
        tag_name = None

        for key, value in definition.items():
            if key == 'id' and value == tag_id:
                tag_name_found = True  # Marca como encontrado el ID
            elif key == 'name' and tag_name_found:
                tag_name = value  # Asigna el nombre del tag
                return tag_name

    return tag_name  # Devuelve tag_name, aunque sea None

'''def extract_names_from_metadata(tag_id, connection_name):
    # Inicializo tag_name por si key == Name pero id no
    tag_name = None

    ###Function to extract the from every tag wiht an ID given from Databus Metadata
    for key,value in metadata_payload.items():
        if (key == 'connections'):
                elements = value
                exit
    for element in elements:
        for key,value in element.items():
            if (key == 'name'):
                if (value == connection_name):
                    continue
                else:
                    break
            if (key == 'dataPoints'):
                dataPoints = value
                exit
    
    for datapoint in dataPoints:
        for key,value in datapoint.items():
            if (key == 'dataPointDefinitions'):
                definitions = value
                exit
    
    for definition in definitions:
        for key,value in definition.items():
            if (key == 'name'):
                tag_name = value
            if (key == 'id'):
                if (value == tag_id):
                    return tag_name'''

def build_json_influx(dict_values, connection_name):
    logging.info('Data are sending to database is:'+ str(dict_values))
    json_fields = (dict_values)
    json_body = [
        {
            "measurement" : connection_name,
            "fields": json_fields
        }
    ]
    logging.info('Data are sending to database is:'+ str(type(json_body)))
    influx_client.write_points(json_body)

def extract_data(topic, payload):
    ###Function to extract values from every tag when a data message is received from Databus
    dict_values = dict()
    ###First we need to identify the connection name
    connection_name = extract_connection_name(topic)
    #Message comes with an id,value for every tag, we need to know which id refers to which tag name
    for key,value in payload.items():
        if (key == 'vals'):
            vals = value
            exit
    for tag in vals:
        for key, value in tag.items():
            if (key== 'id'):
                tag_id = value
                tag_name = extract_names_from_metadata(tag_id, connection_name)
            if (key == 'val'):
                tag_val= value
                dict_values[tag_name] = tag_val

    logging.info('Data are sending to database is:'+ str(type(dict_values)))       
    build_json_influx(dict_values, connection_name)
    
    

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+ str(rc))
    client.subscribe(MQTT_TOPIC_DATA)
    client.subscribe(MQTT_TOPIC_METADATA)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    topic = msg.topic
    if msg.topic == MQTT_TOPIC_METADATA:
        save_metadata(payload)
    elif msg.topic == MQTT_TOPIC_DATA:
        extract_data(topic, payload)
    else:
        logging.info('Unknown topic...')



time.sleep(5)
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(MQTT_USER,MQTT_PASSWORD)
client.connect(MQTT_BROKER_SERVER, 1883, 60)

logging.info('Creating influxdb')

influx_client = InfluxDBClient(INFLUXDB_IP,8086,"root","root",INFLUXDB_DATABASE)

#create a new database and use this database
influx_client.create_database(INFLUXDB_DATABASE)
influx_client.switch_database(INFLUXDB_DATABASE)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()