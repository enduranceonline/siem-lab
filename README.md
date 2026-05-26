# SIEM Lab MVP

## Descripción general

**SIEM Lab MVP** es un laboratorio académico orientado a simular el funcionamiento básico de un sistema SIEM (*Security Information and Event Management*).

El objetivo principal del proyecto es recibir eventos de seguridad, almacenarlos en una base de datos, evaluarlos mediante reglas configurables y generar alertas cuando se cumplen determinadas condiciones.

El proyecto se ha desarrollado como una aplicación web sencilla, modular y contenerizada, utilizando tecnologías habituales en entornos backend y de ciberseguridad defensiva.

Este laboratorio está enfocado al aprendizaje de conceptos relacionados con:

- Ingesta de eventos de seguridad.
- Persistencia de datos en PostgreSQL.
- Exposición de una API REST mediante FastAPI.
- Validación de datos con Pydantic.
- Modelado de datos con SQLAlchemy.
- Gestión de migraciones con Alembic.
- Generación y consulta de alertas.
- Visualización básica mediante frontend web.
- Contenerización del entorno mediante Docker Compose.

---

## Objetivo del proyecto

El objetivo del proyecto es construir un MVP funcional de un laboratorio SIEM que permita demostrar el flujo básico de trabajo de una herramienta de monitorización defensiva:

```text
Evento de seguridad
        ↓
API de ingesta
        ↓
Validación del evento
        ↓
Almacenamiento en PostgreSQL
        ↓
Evaluación mediante reglas
        ↓
Generación de alertas
        ↓
Consulta desde API o frontend
````

El sistema no pretende sustituir a una solución SIEM real, sino servir como laboratorio didáctico para comprender cómo se conectan los principales componentes de una arquitectura de este tipo.

---

## Tecnologías utilizadas

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* Psycopg
* Alembic
* Pytest
* HTTPX

### Base de datos

* PostgreSQL 16

### Frontend

* HTML
* CSS
* JavaScript

### Contenerización

* Docker
* Docker Compose

### Herramientas auxiliares

* Adminer
* Git
* GitHub Actions

---

## Estructura del proyecto

```text
siem-lab/
├── backend/
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   └── pytest.ini
├── frontend/
│   ├── assets/
│   ├── index.html
│   └── alert.html
├── docker/
│   └── compose.yml
├── configs/
├── data/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Componentes principales

### Backend FastAPI

El backend es el núcleo del laboratorio. Expone los endpoints de la API, recibe eventos, consulta la base de datos, evalúa reglas y devuelve respuestas en formato JSON.

El punto de entrada principal es:

```text
backend/app/main.py
```

Desde este archivo se inicializa la aplicación FastAPI y se cargan las rutas principales del sistema.

---

### Base de datos PostgreSQL

La base de datos almacena la información principal del laboratorio:

* Eventos recibidos.
* Reglas de detección.
* Alertas generadas.

Los modelos se encuentran en:

```text
backend/app/models/
```

La conexión y sesiones de base de datos se gestionan desde:

```text
backend/app/db/
```

---

### API de ingesta

La API de ingesta permite introducir eventos de seguridad en el sistema. Estos eventos son validados, almacenados y utilizados posteriormente por el motor de reglas.

Las rutas relacionadas se encuentran en:

```text
backend/app/api/routes/ingest.py
backend/app/api/routes/events.py
```

---

### Motor de reglas

El motor de reglas permite definir condiciones para detectar eventos relevantes. Cuando un evento cumple una regla, el sistema puede generar una alerta.

Las rutas y modelos relacionados se encuentran en:

```text
backend/app/api/routes/rules.py
backend/app/models/rule.py
backend/app/schemas/rule.py
```

---

### Gestión de alertas

La gestión de alertas permite consultar, filtrar y actualizar las alertas generadas por el sistema.

Los archivos relacionados son:

```text
backend/app/api/routes/alerts.py
backend/app/api/routes/metrics.py
backend/app/models/alert.py
backend/app/schemas/alert.py
```

---

### Frontend

El frontend permite visualizar la información del laboratorio desde el navegador sin depender únicamente de Swagger, curl o Adminer.

Los archivos principales son:

```text
frontend/index.html
frontend/alert.html
frontend/assets/app.js
frontend/assets/alerts.js
frontend/assets/alert_detail.js
frontend/assets/styles.css
```

---

### Docker Compose

El entorno se levanta mediante Docker Compose. El archivo principal es:

```text
docker/compose.yml
```

Este archivo define tres servicios principales:

```text
db       → PostgreSQL
adminer  → Interfaz web para consultar la base de datos
api      → Backend FastAPI
```

---

## Requisitos previos

Para ejecutar el proyecto se recomienda tener instalado:

* Docker
* Docker Compose
* Git

Opcionalmente, para ejecutar el backend fuera de Docker:

* Python 3.12
* pip
* entorno virtual de Python

---

## Variables de entorno

El proyecto utiliza variables de entorno para configurar la base de datos, los puertos y la información de versión.

Se incluye el archivo:

```text
.env.example
```

Este archivo sirve como plantilla segura.

Contenido esperado:

```env
POSTGRES_DB=siem
POSTGRES_USER=siem
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql+psycopg://siem:change_me@db:5432/siem

API_PORT=8000
ADMINER_PORT=8080

APP_VERSION=0.1.0
GIT_SHA=unknown
BUILD_TIME=unknown
```

Para preparar el entorno local:

```bash
cp .env.example .env
cp .env.example docker/.env
```

Después se pueden modificar los valores si es necesario.

---

## Ejecución con Docker Compose

Desde la raíz del proyecto:

```bash
cd siem-lab
```

Levantar el laboratorio:

```bash
docker compose --env-file docker/.env -f docker/compose.yml up -d
```

Comprobar los contenedores activos:

```bash
docker ps
```

Servicios esperados:

```text
siem-db       → PostgreSQL
siem-adminer  → Adminer
siem-api      → API FastAPI
```

---

## Acceso a la aplicación

API FastAPI:

```text
http://localhost:8000
```

Documentación Swagger:

```text
http://localhost:8000/docs
```

Adminer:

```text
http://localhost:8080
```

Frontend:

El frontend se encuentra en la carpeta:

```text
frontend/
```

Puede abrirse desde el navegador usando los archivos HTML incluidos en el proyecto.

---

## Comandos útiles

Ver logs de la API:

```bash
docker logs siem-api
```

Ver logs de PostgreSQL:

```bash
docker logs siem-db
```

Ver logs de Adminer:

```bash
docker logs siem-adminer
```

Entrar en el contenedor de la API:

```bash
docker exec -it siem-api bash
```

Entrar en PostgreSQL:

```bash
docker exec -it siem-db psql -U siem -d siem
```

Apagar el laboratorio:

```bash
docker compose --env-file docker/.env -f docker/compose.yml down
```

Apagar el laboratorio eliminando también volúmenes:

```bash
docker compose --env-file docker/.env -f docker/compose.yml down -v
```

---

## Migraciones de base de datos

El proyecto utiliza Alembic para gestionar la evolución de la base de datos.

Las migraciones se encuentran en:

```text
backend/alembic/versions/
```

Ejecutar migraciones desde el contenedor de la API:

```bash
docker exec -it siem-api alembic upgrade head
```

Consultar el estado actual de Alembic:

```bash
docker exec -it siem-api alembic current
```

---

## Tests

El proyecto incluye pruebas automatizadas en:

```text
backend/tests/
```

Ejecutar tests desde la carpeta backend:

```bash
cd backend
pytest
```

Ejecutar tests dentro del contenedor:

```bash
docker exec -it siem-api pytest
```

Los tests permiten validar partes básicas del backend, como la disponibilidad del servicio y el comportamiento de determinadas rutas.

---

## Endpoints principales

Algunos de los endpoints principales del sistema son:

```text
GET  /health
GET  /info
POST /ingest
GET  /events
GET  /rules
POST /rules
GET  /alerts
GET  /metrics
```

La documentación interactiva puede consultarse desde:

```text
http://localhost:8000/docs
```

---

## Flujo general de datos

El flujo principal del laboratorio es el siguiente:

```text
1. Un evento de seguridad entra por la API de ingesta.
2. FastAPI recibe la petición HTTP.
3. Pydantic valida la estructura de los datos.
4. SQLAlchemy guarda el evento en PostgreSQL.
5. El sistema consulta las reglas configuradas.
6. El motor de reglas evalúa si el evento cumple alguna condición.
7. Si se cumple una regla, se genera una alerta.
8. La alerta queda almacenada en PostgreSQL.
9. El usuario puede consultar eventos, reglas, alertas y métricas desde la API o el frontend.
```

---

## Notas sobre la entrega

El archivo ZIP de entrega incluye el código fuente del proyecto, la configuración Docker, el frontend, el backend, las migraciones de base de datos, los tests y la documentación principal del repositorio.

Por motivos de seguridad y limpieza, se han excluido del ZIP los archivos y carpetas generados localmente o asociados al entorno de desarrollo:

```text
.env
docker/.env
.git/
venv/
.venv/
backend/venv/
__pycache__/
.pytest_cache/
*.pyc
```

Los archivos `.env` y `docker/.env` contienen configuración local del entorno, por lo que no se entregan. En su lugar, se incluye `.env.example`, que sirve como plantilla para crear las variables necesarias.

La carpeta `.git/` no se incluye en el ZIP porque pertenece al historial interno del repositorio. Si se requiere consultar el historial de desarrollo, puede utilizarse el repositorio de GitHub asociado al proyecto.

Las carpetas `venv/`, `.venv/`, `backend/venv/`, `__pycache__/`, `.pytest_cache/` y los archivos `*.pyc` son elementos generados localmente por Python, pytest o el entorno de desarrollo, y pueden reconstruirse automáticamente.

---

## Estado del proyecto

El proyecto se encuentra en estado MVP funcional. Permite levantar el entorno mediante Docker Compose, exponer una API backend, almacenar información en PostgreSQL, gestionar eventos, reglas y alertas, y consultar información desde frontend o herramientas auxiliares.

---

## Posibles mejoras futuras

Algunas líneas de mejora futuras serían:

* Añadir autenticación de usuarios.
* Incorporar roles y permisos.
* Mejorar la interfaz frontend.
* Añadir gráficos y dashboards.
* Incorporar más tipos de reglas de correlación.
* Permitir importación de logs desde fuentes externas.
* Añadir integración con herramientas de monitorización.
* Mejorar la cobertura de tests.
* Preparar perfiles diferenciados para desarrollo y producción.
* Añadir despliegue automatizado más completo.

---

## Autor

Proyecto desarrollado como parte del ciclo formativo de Desarrollo de Aplicaciones Multiplataforma.

```

