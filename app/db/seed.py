"""
Script de carga inicial de datos (seed).

Ejecutar UNA SOLA VEZ después de crear las tablas:
    python -m app.db.seed

Inserta datos de catálogos básicos (roles, canales, estados, etc.)
usando los services del proyecto para respetar la lógica de negocio.

NO usar en producción sin revisar los datos primero.
"""

from app.db.database import SessionLocal
from app.schemas.rol_dto import RolCreateDTO
from app.schemas.canal_dto import CanalCreateDTO
from app.schemas.estado_ticket_dto import EstadoTicketCreateDTO
from app.schemas.nivel_impacto_dto import NivelImpactoCreateDTO
from app.schemas.tipo_ticket_dto import TipoTicketCreateDTO
from app.schemas.departamento_dto import DepartamentoCreateDTO
from app.schemas.servicio_dto import ServicioCreateDTO
from app.services.rol_service import rol_service
from app.services.canal_service import canal_service
from app.services.estado_ticket_service import estado_ticket_service
from app.services.nivel_impacto_service import nivel_impacto_service
from app.services.tipo_ticket_service import tipo_ticket_service
from app.services.departament_service import departamento_service
from app.services.servicio_service import servicio_service


def seed_catalogos(db):
    """Inserta datos iniciales de catálogos. Idempotente: no inserta duplicados."""
    inserts = 0

    # ── Roles ───────────────────────────────────────────────────────
    roles = [
        ("Administrador", "Usuario con acceso completo a todas las funcionalidades del sistema."),
        ("Gestor", "Usuario con acceso a la gestión de tickets y clientes."),
        ("Técnico", "Usuario responsable de resolver tickets asignados."),
    ]
    for nombre, descripcion in roles:
        try:
            rol_service.create_rol(db, RolCreateDTO(nombre_rol=nombre, descripcion=descripcion))
            inserts += 1
            print(f"  ✓ Rol creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Rol ya existe: {nombre}")

    # ── Canales ─────────────────────────────────────────────────────
    canales = ["Presencial", "Teléfono", "Correo electrónico", "Portal web"]
    for nombre in canales:
        try:
            canal_service.create_canal(db, CanalCreateDTO(nombre_canal=nombre))
            inserts += 1
            print(f"  ✓ Canal creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Canal ya existe: {nombre}")

    # ── Estados de ticket ───────────────────────────────────────────
    estados = ["Abierto", "En proceso", "Pendiente cliente", "Resuelto", "Cerrado"]
    for nombre in estados:
        try:
            estado_ticket_service.create_estado_ticket(
                db, EstadoTicketCreateDTO(nombre_estado=nombre)
            )
            inserts += 1
            print(f"  ✓ Estado creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Estado ya existe: {nombre}")

    # ── Niveles de impacto ──────────────────────────────────────────
    impactos = [
        ("Bajo", 1),
        ("Medio", 3),
        ("Alto", 5),
        ("Crítico", 10),
    ]
    for nombre, peso in impactos:
        try:
            nivel_impacto_service.create_nivel_impacto(
                db, NivelImpactoCreateDTO(nombre_impacto=nombre, peso_impacto=peso)
            )
            inserts += 1
            print(f"  ✓ Nivel impacto creado: {nombre} (peso={peso})")
        except Exception:
            db.rollback()
            print(f"  - Nivel impacto ya existe: {nombre}")

    # ── Tipos de ticket ─────────────────────────────────────────────
    tipos = ["Incidencia", "Consulta", "Reclamo", "Solicitud de servicio"]
    for nombre in tipos:
        try:
            tipo_ticket_service.create_tipo_ticket(
                db, TipoTicketCreateDTO(nombre_tipo_ticket=nombre)
            )
            inserts += 1
            print(f"  ✓ Tipo ticket creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Tipo ticket ya existe: {nombre}")

    # ── Departamentos ───────────────────────────────────────────────
    departamentos = [
        "Alta Verapaz", "Baja Verapaz", "Chimaltenango", "Chiquimula",
        "El Progreso", "Escuintla", "Guatemala", "Huehuetenango",
        "Izabal", "Jalapa", "Jutiapa", "Petén",
        "Quetzaltenango", "Quiché", "Retalhuleu", "Sacatepéquez",
        "San Marcos", "Santa Rosa", "Sololá", "Suchitepéquez",
        "Totonicapán", "Zacapa",
    ]
    for nombre in departamentos:
        try:
            departamento_service.create_departamento(
                db, DepartamentoCreateDTO(nombre_departamento=nombre)
            )
            inserts += 1
            print(f"  ✓ Departamento creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Departamento ya existe: {nombre}")

    # ── Servicios ───────────────────────────────────────────────────
    servicios = [
        "Internet residencial",
        "Internet empresarial",
        "Televisión por cable",
        "Telefonía fija",
        "Telefonía móvil",
    ]
    for nombre in servicios:
        try:
            servicio_service.create_servicio(
                db, ServicioCreateDTO(nombre_servicio=nombre)
            )
            inserts += 1
            print(f"  ✓ Servicio creado: {nombre}")
        except Exception:
            db.rollback()
            print(f"  - Servicio ya existe: {nombre}")

    db.commit()
    return inserts


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("🌱 Insertando datos iniciales (seed)...")
        total = seed_catalogos(db)
        print(f"\n✅ Seed completado. {total} registros insertados.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante el seed: {e}")
    finally:
        db.close()