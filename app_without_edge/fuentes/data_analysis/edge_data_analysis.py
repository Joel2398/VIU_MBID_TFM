import json
import pandas as pd
from influxdb import InfluxDBClient
import logging

logging.getLogger().setLevel(logging.INFO)

# Leer archivo de configuración
def readFile(filename):
    with open('/cfg-data/'+filename) as f:
        data = json.load(f)
        logging.info('File successfully read')
        return data

# Cargar configuración
data = readFile('env-config.json')
INFLUXDB_IP = data['env']['INFLUXDB_IP']
INFLUXDB_DATABASE = data['env']['INFLUXDB_DATABASE']

def fetch_data_from_influxdb():
    # Crear cliente de InfluxDB
    client = InfluxDBClient(INFLUXDB_IP, 8086, "root", "root", INFLUXDB_DATABASE)
    
    # Consulta de datos (modifica según tus necesidades)
    query = 'SELECT * FROM "PLC_1" WHERE time > now() - 1h'
    
    # Ejecutar consulta
    result = client.query(query)
    points = list(result.get_points())
    
    # Convertir puntos a DataFrame
    df = pd.DataFrame(points)
    
    # Cerrar cliente
    client.close()
    
    return df

# Uso del script
if __name__ == "__main__":
    df = fetch_data_from_influxdb()
    print(df.head())  # Mostrar las primeras filas del DataFrame
