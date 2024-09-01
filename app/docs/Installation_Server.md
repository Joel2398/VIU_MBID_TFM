 # Aplicación local

  - [Pasos de instalación](#pasos-de-instalación)
    - [Instalación](#instalación)
    - [Configuración de tagdata](#Configuración-de-tagdata)
    - [Build y Deploy de la aplicación](#build-y-deploy-de-la-aplicación)

## Configuración de tagdata
Para poder simular todo desde una máquina debemos utilizar node-red y simular un MQTT Broker
Para ello lo que he hecho ha sido crear el broker y simular unos topic que me emularán el databus
Mirando la documentación, vemos la estructura del JSON
![JSON Structure for tags data. Fuente: OPC UA COnnector V2.1.0](app/docs/graficos/JSON_Structure_tag_Data_OPCUAConnector_V2_1_0.png)
