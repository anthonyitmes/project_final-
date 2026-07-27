"""
Configuración de Alembic para el proyecto project_final.

Conexión a la BD: toma la URL desde app.core.config (que lee .env).
Modelos: importa todos los modelos para que Base.metadata los conozca
         y --autogenerate pueda detectar cambios automáticamente.
"""

import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

# ── 1. Agregar la raíz del proyecto al sys.path ─────────────────────
# Necesario para que 'from app...' funcione cuando Alembic se ejecuta
# desde cualquier directorio.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# ── 2. Configuración de logging desde alembic.ini ───────────────────
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── 3. Importar Base y TODOS los modelos ────────────────────────────
# Base.metadata contiene la definición de las 14 tablas.
# Es obligatorio importar cada modelo para que SQLAlchemy los registre.
from app.db.database import Base
from app.core.config import settings

# Todos los modelos (necesarios para autogenerate)
import app.models.canales                    # noqa: F401
import app.models.clientes                   # noqa: F401
import app.models.clientes_servicios         # noqa: F401
import app.models.departamentos              # noqa: F401
import app.models.direcciones                # noqa: F401
import app.models.empleados                 # noqa: F401
import app.models.estado_ticket              # noqa: F401
import app.models.municipios                # noqa: F401
import app.models.niveles_impacto            # noqa: F401
import app.models.plantilla_formulario       # noqa: F401
import app.models.roles                     # noqa: F401
import app.models.servicios                 # noqa: F401
import app.models.tickets                   # noqa: F401
import app.models.tipos_ticket              # noqa: F401

# ── 4. Metadata para autogenerate ───────────────────────────────────
target_metadata = Base.metadata

# ── 5. URL de la BD desde config.py (lee .env) ─────────────────────
DATABASE_URL = settings.DATABASE_URL


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline' (genera SQL sin conectar a la BD).

    Útil para revisar el SQL antes de aplicarlo o para entornos sin BD disponible.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' (conecta a la BD real).

    Crea un engine con la URL de settings, se conecta, y aplica las migraciones.
    """
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# ── 6. Punto de entrada ─────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()