# Aplicación de test con Grafanaa, InfluxDB y Broker MQTT simulado

Se lleva a cabo aplicación multiservicio en entorno de test. Con el objetivo de probar y emular lo que posteriormente se desplegará sobre un equipo EDGE

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Conclusiones](#conclusiones)
- [Documentación](#documentación)
- [Futuros Pasos](#futuros-pasos)
- [Colaboración](#colaboración)
- [Autores](#autores)
- [Licencias](#licencias)

## Descripción

En el ejemplo se reciben datos por S7 de un PLC y se almacenan en la base de datos InfluxDB y se visualizan en Grafana.
Se crea una aplicación que contiene tres servicios:
- Servicio en Python con cliente MQTT que se conecta al Databus para recibir los datos de un PLC mediante la conexión S7, después este servicio se conecta a la base de datos y los inserta.
- Base de datos InfluxDB
- Grafana

En el ejemplo se explica como ejecutar la aplicación de manera local y cómo instalarla en el Edge Device.

## Requisitos

### Prerequesitos
- Industrial Edge Management instalado.
- MV Linux Vcon docker y docker-compose instalado.
- Industrial Edge App Publisher instalado en una máquina con acceso en red al IEM y a la MV de linux.
- Edge Devices arrancados con IP y MAC conocidas de antemano.
- Databus instalado y arrancado
- Flow Creator instalado y arrancado

### Componentes usados

- VM Ubuntu 20.04
- Docker 20.10.21

### HW utilizado

- Todos los servicios se levantan mediante VM Ubuntu
- La simulación del PLC se realiza con PLCSIM y NetToPLC

## Casos de uso

- [Aplicación en servidor externo](docs/Installation_Server.md)
- [Aplicación en IED](docs/Installation_Device.md)


## Conclusiones




## Documentación 

- [Industrial Edge Hub](https://iehub.eu1.edge.siemens.cloud/#/documentation)
- [Industrial Edge Forum](https://www.siemens.com/industrial-edge-forum)
- [Industrial Edge landing page](https://new.siemens.com/global/en/products/automation/topic-areas/industrial-edge/simatic-edge.html)
- [Industrial Edge App Developer Documentation](https://industrial-edge.io/developer/index.html)

## Colaboración



## Futuros Pasos


## Autores
Joel J Rojas Gonzalez

## Licencias
