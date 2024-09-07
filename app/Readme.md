# Ejemplo de aplicación de Grafana e InfluxDB

Guía rápida en español de cómo implementar una aplicación multiservicio con Grafana e InfluxDB 

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

- Industrial Edge Device  V ____ (API version ____)
- Industrial Edge Management App V ____ (API version ____)
- Industrial Edge Publisher V ____
- VM Ubuntu 20.04
- Docker 20.10.21

### HW utilizado

- IPC 227E 6ES7647-8BD31-0CW1

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

- Subid los cambios a una rama de Pred-Prod
- Solicitad los cambios a la main con un merge-request


## Futuros Pasos

Probar para múltiples tipos de IEDs: No sabemos si no está preparado o que en está aplicación no se saca la info del tipo de IEDS.
En la API del IEM, para crear un IED nuevo, no sale nada de un identificador por tipo de IED, por lo que la API solo está preparada para dar de alta 227E.


Generar dos tareas para:
- Incluir un descubrimiento en los equipos?
- Generar el excel de manera automática.


## Autores
Mariola Belda Marín
RC-ES DI FA Dir Tech. Siemens S.A. 

## Licencias
