# WhatsApp Survey API

Esta es una API desarrollada con FastAPI para gestionar encuestas a través de WhatsApp.

## Características

- Envio y recepción de respuestas mediante WhatsApp.
- Integración con bases de datos para almacenar resultados.
- Endpoints documentados con OpenAPI.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes requisitos:

- Python 3.10+
- `pip` y `venv` para la gestión de paquetes

## Instalación y Ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/whatsapp-survey-api.git
   cd whatsapp-survey-api
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables:

   ```ini
   TWILIO_API_KEY=tu_api_key
   DATABASE_URL=sqlite:///./database.db  # O la URL de tu base de datos
   ```

5. Ejecuta la aplicación:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload
   ```

6. Accede a la documentación de la API:
   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [Redoc](http://127.0.0.1:8000/redoc)

## Tecnologías utilizadas

- FastAPI
- Uvicorn
- SQLAlchemy
- Twilio API
- JWT
