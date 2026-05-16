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
│   │   ├── api/routes/
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

## 7. URLs principales

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

## 8. Credenciales de base de datos

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

## 9. Endpoints principales

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

## 10. Funcionamiento del motor de reglas

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

## 11. Ejemplo de ingesta de evento

Ejemplo de evento compatible con una regla de SSH:

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

## 12. Consulta de alertas

Consulta de las últimas alertas enriquecidas:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?limit=5" | python3 -m json.tool
```

Filtros disponibles:

```bash
curl -s "http://127.0.0.1:8000/alerts/ui?status=ack" | python3 -m json.tool
curl -s "http://127.0.0.1:8000/alerts/ui?severity_min=7" | python3 -m json.tool
curl -s "http://127.0.0.1:8000/alerts/ui?q=failed" | python3 -m json.tool
```

---

## 13. Actualización de estado de alerta

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

---

## 14. Frontend

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

## 15. Adminer

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

## 16. Pruebas automatizadas

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

---

## 17. Validación funcional realizada

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

## 18. Limitaciones

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

## 19. Futuras mejoras

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

## 20. Conclusión

SIEM Lab demuestra el funcionamiento básico de un sistema de monitorización de seguridad: recepción de eventos, almacenamiento, evaluación mediante reglas, generación automática de alertas y consulta posterior.

Aunque se trata de un MVP académico, el proyecto permite comprender de forma práctica conceptos fundamentales del Blue Team y sirve como base para futuras ampliaciones hacia un laboratorio de ciberseguridad más completo.
