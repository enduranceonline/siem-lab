# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.info import router as info_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.rules import router as rules_router

app = FastAPI(title="SIEM Backend", version="0.1.0")

# CORS (DEV): permite el frontend servido localmente.
# Ajusta el/los orígenes a tu puerto real (p.ej. 5173 si usas Vite).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(events_router)
app.include_router(ingest_router)
app.include_router(rules_router)
app.include_router(alerts_router)
app.include_router(info_router)
app.include_router(metrics_router)
