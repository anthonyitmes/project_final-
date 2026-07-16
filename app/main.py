from fastapi import FastAPI

# ── Importar routers ─────────────────────────────────────────────────
# Cada archivo exporta "router", lo renombramos con "as x_router"
# para que sea legible y no haya colisión de nombres.
from app.api.routers.canal_router import router as canal_router
from app.api.routers.cliente_router import router as cliente_router
from app.api.routers.cliente_servicio_router import router as cliente_servicio_router
from app.api.routers.departamento_router import router as departamento_router
from app.api.routers.direccion_router import router as direccion_router
from app.api.routers.empleado_router import router as empleado_router
from app.api.routers.estado_ticket_router import router as estado_ticket_router
from app.api.routers.municipio_router import router as municipio_router
from app.api.routers.nivel_impacto_router import router as nivel_impacto_router
from app.api.routers.plantilla_formulario_router import router as plantilla_formulario_router
from app.api.routers.rol_router import router as rol_router
from app.api.routers.servicio_router import router as servicio_router
from app.api.routers.ticket_router import router as ticket_router
from app.api.routers.tipo_ticket_router import router as tipo_ticket_router
from app.api.routers.auth_router import router as auth_router

app = FastAPI(title="project_final")
fastapi_app = app

# ── Registrar routers ────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(canal_router)
app.include_router(cliente_router)
app.include_router(cliente_servicio_router)
app.include_router(departamento_router)
app.include_router(direccion_router)
app.include_router(empleado_router)
app.include_router(estado_ticket_router)
app.include_router(municipio_router)
app.include_router(nivel_impacto_router)
app.include_router(plantilla_formulario_router)
app.include_router(rol_router)
app.include_router(servicio_router)
app.include_router(ticket_router)
app.include_router(tipo_ticket_router)


@app.get("/")
def read_root():
    return {"message": "API project_final funcionando"}