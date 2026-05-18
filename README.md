# SIEM Lab MVP

Mini SIEM educativo desarrollado como proyecto de DAM con enfoque Blue Team.

El objetivo del proyecto es simular el flujo básico de un sistema SIEM: ingesta de eventos, evaluación mediante reglas, generación automática de alertas, consulta de alertas y visualización básica mediante frontend.

---

## 1. Descripción general

**SIEM Lab** es una aplicación web compuesta por un backend desarrollado con FastAPI, una base de datos PostgreSQL, un frontend sencillo en HTML/CSS/JavaScript y un entorno de ejecución basado en Docker Compose.

El sistema permite recibir eventos de seguridad simulados, almacenarlos en base de datos, evaluarlos mediante reglas activas y generar alertas cuando se cumplen determinadas condiciones.

El proyecto está planteado como un **MVP académico**, no como una herramienta SIEM de producción. Su finalidad principal es demostrar de forma práctica conceptos básicos relacionados con la monitorización de seguridad, la ingesta de logs, la correlación sencilla mediante reglas y la gestión de alertas.

---

## 2. Objetivos del proyecto

Los objetivos principales del proyecto son:

- Diseñar una arquitectura básica de tipo SIEM.
- Crear una API REST para gestionar eventos, reglas y alertas.
- Almacenar la información en una base de datos PostgreSQL.
- Implementar un motor de reglas sencillo.
- Generar alertas automáticamente a partir de eventos ingestados.
- Permitir la consulta y filtrado de alertas.
- Permitir el cambio de estado de una alerta.
- Crear un frontend básico para visualizar las alertas.
- Contenerizar el entorno mediante Docker Compose.
- Validar el funcionamiento mediante pruebas automatizadas.

---

## 3. Stack tecnológico

El proyecto utiliza las siguientes tecnologías:

- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL 16
- SQLAlchemy
- Alembic
- Docker Compose
- Adminer
- HTML
- CSS
- JavaScript
- Pytest

---

## 4. Arquitectura del sistema

El entorno se levanta mediante Docker Compose e incluye tres servicios principales:

```text
siem-db       → Base de datos PostgreSQL
siem-api      → API REST desarrollada con FastAPI
siem-adminer  → Interfaz web para consultar la base de datos
```

El flujo principal del sistema es el siguiente:

```text
Evento/log simulado
        ↓
POST /ingest
        ↓
Almacenamiento en PostgreSQL
        ↓
Evaluación mediante reglas activas
        ↓
Generación automática de alerta
        ↓
Consulta mediante API o frontend
```

---

## 5. Estructura del proyecto

```text
siem-lab/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── db/
│   │   ├── models/
│   │   └── schemas/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── index.html
│   ├── alert.html
│   └── assets/
│       ├── alerts.js
│       ├── alert_detail.js
│       ├── app.js
│       └── styles.css
│
├── docker/
│   ├── compose.yml
│   └── .env
│
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

## 6. Puesta en marcha

Desde la raíz del proyecto:

```bash
docker compose -f docker/compose.yml up -d --build
```

También puede ejecutarse desde la carpeta `docker`:

```bash
cd docker
docker compose up -d --build
```

Para comprobar el estado de los contenedores:

```bash
docker compose ps
```

Servicios esperados:

```text
siem-db        Up / Healthy
siem-api       Up
siem-adminer   Up
```

---

## 7. Reproducción desde cero

Para reproducir el proyecto en otro equipo desde cero, es necesario tener instalado:

- Git
- Docker
- Docker Compose
- Navegador web
- Python 3, solo si se quiere servir el frontend con `http.server`

### 7.1. Clonar el repositorio

```bash
git clone https://github.com/enduranceonline/siem-lab.git
cd siem-lab
```

### 7.2. Crear archivos de entorno

Los archivos `.env` reales no se suben al repositorio por seguridad.

Para crear la configuración local a partir del ejemplo:

```bash
cp .env.example .env
cp .env.example docker/.env
```

Los valores por defecto para laboratorio son:

```text
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

### 7.3. Levantar el entorno

Desde la raíz del proyecto:

```bash
docker compose -f docker/compose.yml up -d --build
```

También puede hacerse desde la carpeta `docker`:

```bash
cd docker
docker compose up -d --build
```

### 7.4. Comprobar contenedores

Desde la raíz del proyecto:

```bash
docker compose -f docker/compose.yml ps
```

Si se está dentro de la carpeta `docker`:

```bash
docker compose ps
```

Deben aparecer los servicios:

```text
siem-db
siem-api
siem-adminer
```

### 7.5. Ejecutar migraciones

Si la base de datos está vacía, ejecutar las migraciones de Alembic:

```bash
docker compose -f docker/compose.yml exec api alembic upgrade head
```

Si se está dentro de la carpeta `docker`:

```bash
docker compose exec api alembic upgrade head
```

### 7.6. Comprobar la API

```bash
curl http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "db": "ok"
}
```

También se puede abrir Swagger:

```text
http://127.0.0.1:8000/docs
```

### 7.7. Crear una regla de demo

```bash
curl -X POST http://127.0.0.1:8000/rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSH failed login demo",
    "enabled": true,
    "source": "ssh",
    "severity_min": 5,
    "contains": "failed",
    "meta_match": null,
    "throttle_seconds": 60,
    "threshold_count": null,
    "threshold_seconds": null
  }'
```

### 7.8. Enviar un evento de demo

```bash
HOST="demo-$(date +%s)"

curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d "{
    \"source\": \"ssh\",
    \"severity\": 7,
    \"message\": \"failed password for invalid user demo\",
    \"meta\": {
      \"host\": \"$HOST\"
    }
  }"
```

### 7.9. Consultar alertas generadas

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?limit=5" | python3 -m json.tool
```

Si todo funciona correctamente, aparecerá una alerta generada automáticamente a partir del evento enviado por `/ingest`.

### 7.10. Servir el frontend

En otra terminal:

```bash
cd siem-lab
python3 -m http.server 5173 -d frontend
```

Abrir en el navegador:

```text
http://127.0.0.1:5173/index.html
```

### 7.11. Acceder a Adminer

```text
http://127.0.0.1:8080
```

Credenciales:

```text
Sistema: PostgreSQL
Servidor: db
Usuario: siem
Contraseña: change_me
Base de datos: siem
```

### 7.12. Ejecutar tests

Desde la raíz del proyecto:

```bash
docker compose -f docker/compose.yml exec api python -m pytest
```

Si se está dentro de la carpeta `docker`:

```bash
docker compose exec api python -m pytest
```

Resultado esperado:

```text
4 passed
```

Con estos pasos, el proyecto puede reproducirse desde cero en otro equipo sin depender de archivos locales no incluidos en el repositorio.

---

## 8. URLs principales

Documentación interactiva de la API con Swagger:

```text
http://127.0.0.1:8000/docs
```

Adminer:

```text
http://127.0.0.1:8080
```

Frontend:

```text
http://127.0.0.1:5173/index.html
```

---

## 9. Credenciales de base de datos

Credenciales usadas en el entorno de desarrollo:

```text
Sistema: PostgreSQL
Servidor: db
Usuario: siem
Contraseña: change_me
Base de datos: siem
```

Estas credenciales están pensadas únicamente para un entorno local de laboratorio.

---

## 10. Endpoints principales

### Healthcheck

```http
GET /health
```

Comprueba que la API y la conexión con PostgreSQL funcionan correctamente.

Ejemplo de respuesta:

```json
{
  "status": "ok",
  "db": "ok"
}
```

### Información de la aplicación

```http
GET /info
```

Devuelve información básica de la aplicación, como nombre, versión, commit y hora actual en UTC.

### Eventos

```http
POST /events
GET /events
```

Permite crear y listar eventos simples.

Este endpoint almacena eventos, pero no es el flujo principal de generación de alertas.

### Ingesta

```http
POST /ingest
```

Es el endpoint principal del sistema.

Recibe un evento, lo almacena en la base de datos y ejecuta el motor de reglas. Si el evento cumple las condiciones de una regla activa, se genera una alerta automáticamente.

### Reglas

```http
POST /rules
GET /rules
```

Permite crear y listar reglas de detección.

Una regla puede contener condiciones como:

- Nombre.
- Estado activo/inactivo.
- Source.
- Severidad mínima.
- Texto contenido en el mensaje.
- Coincidencias en metadatos.
- Throttle.
- Threshold.

### Alertas

```http
GET /alerts
GET /alerts/ui
GET /alerts/ui/count
GET /alerts/{alert_id}
GET /alerts/{alert_id}/ui
PATCH /alerts/{alert_id}
```

Permite consultar alertas, ver información enriquecida y actualizar su estado.

El endpoint `/alerts/ui` devuelve información enriquecida combinando datos de alertas, reglas y eventos.

### Métricas

```http
GET /metrics
```

Devuelve métricas básicas del sistema:

- Total de eventos.
- Total de reglas.
- Reglas activas.
- Total de alertas.
- Alertas por estado.
- Alertas agrupadas por `group_key`.

---

## 11. Funcionamiento del motor de reglas

El motor de reglas se ejecuta cuando se recibe un evento mediante:

```http
POST /ingest
```

El proceso interno es:

```text
1. La API recibe un evento.
2. El evento se guarda en PostgreSQL.
3. Se consultan las reglas activas.
4. Cada regla se compara con el evento recibido.
5. Si el evento cumple las condiciones de una regla, se genera una alerta.
6. La alerta queda asociada al evento y a la regla correspondiente.
```

Las condiciones que puede evaluar una regla son:

```text
source
severity_min
contains
meta_match
threshold_count
threshold_seconds
throttle_seconds
```

Además, el sistema usa `meta.host` como `group_key` para agrupar alertas por host o equipo origen.

---

## 12. Ejemplo de regla

Ejemplo de regla para detectar intentos fallidos de autenticación SSH:

```bash
curl -X POST http://127.0.0.1:8000/rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSH failed login",
    "enabled": true,
    "source": "ssh",
    "severity_min": 5,
    "contains": "failed",
    "meta_match": null,
    "throttle_seconds": 60,
    "threshold_count": null,
    "threshold_seconds": null
  }'
```

Esta regla indica que cualquier evento con:

```text
source = ssh
severity >= 5
message contiene "failed"
```

puede generar una alerta.

---

## 13. Ejemplo de ingesta de evento

Ejemplo de evento compatible con la regla anterior:

```bash
HOST="demo-$(date +%s)"

curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d "{
    \"source\": \"ssh\",
    \"severity\": 7,
    \"message\": \"failed password for invalid user demo\",
    \"meta\": {
      \"host\": \"$HOST\"
    }
  }"
```

Si existe una regla activa compatible, el sistema genera una alerta automáticamente.

---

## 14. Consulta de alertas

Consulta de las últimas alertas enriquecidas:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?limit=5" | python3 -m json.tool
```

Ejemplo de alerta generada:

```json
{
  "id": 6,
  "rule_id": 7,
  "event_id": 17,
  "title": "Rule matched: test_rule_ssh",
  "group_key": "demo-1778929393",
  "status": "ack",
  "rule_name": "test_rule_ssh",
  "event_source": "ssh",
  "event_severity": 7,
  "event_message": "failed password for invalid user demo"
}
```

---

## 15. Filtros de alertas

Filtrar por estado:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?status=ack" | python3 -m json.tool
```

Filtrar por severidad mínima:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?severity_min=7" | python3 -m json.tool
```

Buscar por texto:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?q=failed" | python3 -m json.tool
```

Limitar resultados:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?limit=5" | python3 -m json.tool
```

---

## 16. Actualización de estado de una alerta

El sistema permite cambiar el estado de una alerta mediante:

```http
PATCH /alerts/{alert_id}
```

Ejemplo:

```bash
curl -X PATCH http://127.0.0.1:8000/alerts/6 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "ack"
  }'
```

Estados contemplados:

```text
open
ack
closed
```

Esto permite simular una gestión básica del ciclo de vida de una alerta.

---

## 17. Frontend

El frontend se encuentra en la carpeta:

```text
frontend/
```

Para servirlo en local:

```bash
cd ~/siem-lab
python3 -m http.server 5173 -d frontend
```

Después abrir en el navegador:

```text
http://127.0.0.1:5173/index.html
```

La interfaz permite:

- Consultar alertas.
- Aplicar filtros.
- Navegar por resultados.
- Ver el estado de cada alerta.
- Acceder al detalle de una alerta.

---

## 18. Adminer

Adminer permite consultar visualmente la base de datos PostgreSQL.

URL:

```text
http://127.0.0.1:8080
```

Tablas principales:

```text
alembic_version
alerts
events
rules
```

Estas tablas permiten comprobar que los eventos, reglas y alertas quedan persistidos en la base de datos.

---

## 19. Pruebas automatizadas

El proyecto incluye pruebas automatizadas con `pytest`.

Para ejecutarlas dentro del contenedor de la API:

```bash
cd docker
docker compose exec api python -m pytest
```

Resultado validado:

```text
4 passed
```

Las pruebas verifican el funcionamiento de endpoints principales como `/health` y la consulta de alertas orientada a la interfaz.

---

## 20. Validación funcional realizada

Durante la validación del proyecto se comprobó:

```text
[OK] La VM arranca correctamente en VirtualBox.
[OK] Docker Compose levanta los servicios principales.
[OK] PostgreSQL funciona correctamente.
[OK] Adminer permite visualizar la base de datos.
[OK] FastAPI responde en /docs.
[OK] /health responde correctamente.
[OK] /metrics devuelve métricas del sistema.
[OK] /rules lista reglas existentes.
[OK] /ingest permite enviar eventos/logs simulados.
[OK] El motor de reglas genera alertas automáticamente.
[OK] /alerts/ui muestra alertas enriquecidas.
[OK] PATCH /alerts/{id} permite cambiar el estado de una alerta.
[OK] Los filtros por estado, severidad y texto funcionan.
[OK] El frontend carga correctamente y muestra las alertas.
[OK] Los tests automatizados se ejecutan correctamente.
```

---

## 21. Limitaciones

Este proyecto es un MVP educativo. Sus principales limitaciones son:

- No captura logs reales de sistemas externos.
- No incluye agentes de recolección.
- No implementa autenticación de usuarios.
- No incluye roles ni permisos.
- No realiza correlación avanzada como un SIEM empresarial.
- No incluye dashboards avanzados con gráficas.
- No implementa despliegue en producción.
- No sustituye herramientas como Wazuh, Splunk, Elastic SIEM o Microsoft Sentinel.

---

## 22. Futuras mejoras

Posibles ampliaciones del proyecto:

- Integración con logs reales de Linux, Windows o servidores web.
- Integración con agentes como Wazuh.
- Incorporación de Suricata o Zeek para eventos de red.
- Dashboard con gráficas.
- Sistema de usuarios y autenticación.
- Gestión de roles y permisos.
- Reglas más avanzadas.
- Correlación entre múltiples eventos.
- Exportación de informes.
- Contenerización completa del frontend.
- Despliegue en un servidor dedicado o entorno cloud.
- Integración con herramientas de notificación como correo, Telegram o Slack.

---

## 23. Conclusión

SIEM Lab demuestra el funcionamiento básico de un sistema de monitorización de seguridad: recepción de eventos, almacenamiento, evaluación mediante reglas, generación automática de alertas y consulta posterior.

Aunque se trata de un MVP académico, el proyecto permite comprender de forma práctica conceptos fundamentales del Blue Team y sirve como base para futuras ampliaciones hacia un laboratorio de ciberseguridad más completo.
