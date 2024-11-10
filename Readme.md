# TFM - Edge Computing

## Descripción

Este repositorio contiene el trabajo de fin de máster (TFM) desarrollado por **Joel Rojas González** en el ámbito de **Edge Computing**. El objetivo de este proyecto es explorar y desarrollar soluciones innovadoras que aprovechen las capacidades del Edge Computing para mejorar el procesamiento de datos, reducir la latencia y optimizar el uso de recursos en entornos distribuidos.

## Objetivos del Proyecto

- **Investigación del Estado del Arte**: Análisis de las tecnologías actuales de Edge Computing, su evolución, y su aplicación en diversas industrias.
- **Diseño y Desarrollo de Soluciones**: Creación de prototipos que implementen algoritmos de procesamiento de datos en el edge.
- **Evaluación de Rendimiento**: Comparación de soluciones de Edge Computing con otras arquitecturas tradicionales, como la computación en la nube.
- **Implementación Práctica**: Despliegue de un sistema en un entorno de prueba para validar los resultados obtenidos y medir el impacto.

## Estructura del Repositorio

Este repositorio sigue la estructura habitual de proyectos en GitHub, con un archivo `README.md` que proporciona una descripción detallada de la distribución del repositorio. A continuación, se detalla la estructura de carpetas utilizada:

```plaintext
├── app/
│   ├── docs/
│   │   └── documentación_relevante.md
│   ├── src/
│   │   ├── docker-compose.yml
│   │   ├── influxdb/
│   │   │   ├── Dockerfile
│   │   │   └── setup_influxdb.sh
│   │   └── mqtt_client/
│   │       ├── app.py
│   │       ├── requirements.txt
│   │       └── Dockerfile
├── app_without_edge/
│   ├── docs/
│   ├── src/
│   │   ├── docker-compose.yml
│   │   ├── mqtt_client/
│   │   │   ├── app.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── influxdb/
│   │   │   ├── Dockerfile
│   │   │   └── setup_influxdb.sh
│   │   ├── env-config.json
├── data_analysis/
│   ├── data/
│   │   ├── raw_data/
│   │   │   ├── dataset.csv
│   │   │   ├── features.csv
│   │   │   └── labels.csv
│   ├── models/
│   │   ├── model_training.ipynb
│   │   ├── model.pkl
│   │   └── scaler.pkl
│   └── notebooks/
│       ├── exploratory_data_analysis.ipynb
│       └── predictive_analysis.ipynb
└── README.md
```

## Descripción de las Carpetas

- **`app/`**: Esta carpeta contiene los archivos necesarios para hacer funcionar la aplicación dentro de un entorno de Edge Computing.
  - **`docs/`**: Documentación del repositorio.
  - **`src/`**: Carpeta principal con todos los componentes y configuraciones necesarias para ejecutar la aplicación en un entorno Docker. Incluye servicios como InfluxDB y MQTT Client, junto con sus archivos de configuración.

- **`app_without_edge/`**: Similar a la carpeta `app`, pero optimizada para entornos sin Edge Computing. Esta versión permite simular la aplicación en un entorno local, facilitando la validación y depuración antes del despliegue en producción. Aqui simulamos un MQTT Broker que nos permite realizar realizar las simulaciones de entrada y análisis de datos con entrada de datos sintéticas o a partir de una muestra

- **`data_analysis/`**: Aquí se encuentran los archivos necesarios para el análisis de datos basados en una instalación real.
  - **data/**: Almacena los conjuntos de datos utilizados para el análisis.
  - **models/**: Contiene los modelos de predicción entrenados y los archivos de preprocesamiento.
  - **notebooks/**: Incluye Jupyter Notebooks para realizar análisis exploratorios y predictivos.

## Tecnologías Utilizadas

- **Lenguajes de Programación**: Python
- **Frameworks y Bibliotecas**: Scikit-Learn, Pandas, Numpy
- **Plataformas de Edge Computing**: Siemens Industrial Edge
- **Herramientas de Contenedores**: Docker, Docker Compose

## ¿Qué es Edge Computing?

Edge Computing es un paradigma que acerca el procesamiento de datos y la ejecución de aplicaciones a los dispositivos que generan los datos, en lugar de depender de una infraestructura centralizada. Esto permite reducir la latencia, ahorrar ancho de banda, mejorar la seguridad, y posibilitar nuevas aplicaciones en tiempo real.

## Sobre el Autor

Soy **Joel Rojas González**, estudiante de Máster en Big Data y Data Science en la VIU. Mi pasión por la tecnología y mi interés por la computación distribuida y la inteligencia artificial me llevaron a elegir este tema para mi TFM. A través de este trabajo, busco contribuir a la evolución del Edge Computing y su aplicabilidad en la industria.

## Contacto

- **Email**: [joel.rojas2398@gmail.com](mailto:joel.rojas2398@gmail.com)
- **LinkedIn**: [Joel J Rojas González](https://www.linkedin.com/in/joel-j-rojas-gonzález/)
