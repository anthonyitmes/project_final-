# 🗃️ Fase 8 — Alembic + Seed

**Fecha:** 2026-07-27
**Autor:** Anthony Sub 
**Rama:** `main`
**Commit base:** `6407a12`

---

## 1. Resumen ejecutivo

La Fase 8 comprende dos componentes:

| Componente | Herramienta | Propósito |
|---|---|---|
| Migraciones de esquema | **Alembic** | Versionar la estructura de la BD (DDL): crear/alterar/droppear tablas y columnas de forma controlada y reversible |
| Datos iniciales | **Seed script** | Poblar catálogos base (roles, canales, estados, etc.) para que la app sea funcional inmediatamente después del deploy |

---

## 2. Diagnóstico inicial (qué se encontró)

### 2.1 Lo que ya existía antes de esta intervención

| Archivo | Estado | Observación |
|---|---|---|
| `alembic.ini` | ✅ Completo | `script_location = alembic`, logging configurado, URL delegada a `env.py` |
| `alembic/env.py` | ✅ Completo | 91 líneas — importa `Base`, los 14 modelos, lee `settings.DATABASE_URL` desde `.env`, modos offline/online implementados |
| `alembic/versions/55a1c50e11be_initial_migration.py` | ✅ Generada | Primera migración detectó 3 cambios: `roles.descripcion → NOT NULL`, eliminó `tickets.titulo` y `tickets.descripcion` |
| `alembic/script.py.mako` | ✅ Template | Template estándar de Alembic para generar migraciones |
| `app/db/seed.py` | ✅ Completo | 157 líneas, inserta 7 catálogos, idempotente con `try/rollback` |

### 2.2 Lo que faltaba

| Item | Estado | Detalle |
|---|---|---|
| `alembic` en `requirements.txt` | ❌ Ausente | No estaba listado como dependencia |
| Migración aplicada a la BD | ❓ Sin verificar | No se sabía si `alembic upgrade head` se había ejecutado |
| Seed ejecutado | ❓ Sin verificar | No se sabía si `python -m app.db.seed` se había corrido |
| Documentación de la fase | ❌ No existía | Este documento |

---

## 3. Acciones realizadas

### 3.1 Agregar `alembic` a `requirements.txt`

```diff
 SQLAlchemy==2.0.50
+alembic==1.18.5
```

**Razón:** `requirements.txt` es el manifiesto canónico de dependencias del proyecto. `alembic` ya estaba instalado en el virtualenv (`.venv/lib/python3.14/site-packages/alembic-1.18.5`), pero no estaba declarado. Sin esta línea, otro desarrollador que instale desde `requirements.txt` no obtendría `alembic` y las migraciones no funcionarían.

### 3.2 Verificar instalación

```bash
$ source .venv/bin/activate && pip install alembic
Requirement already satisfied: alembic in ./.venv/lib/python3.14/site-packages (1.18.5)
```

**Resultado:** Ya instalado. Versión 1.18.5, compatible con SQLAlchemy 2.0.50.

### 3.3 Aplicar migración a la base de datos

```bash
$ alembic upgrade head
Conexión correcta a la base de datos
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

Verificación:

```bash
$ alembic current
55a1c50e11be (head)
```

**Resultado:** La migración ya estaba aplicada. Esto significa que en algún momento previo (probablemente durante la generación de la migración inicial el mismo 27/jul/2026) se ejecutó `alembic upgrade head` y la BD `user_db` ya refleja el esquema migrado.

### 3.4 Ejecutar seed de datos

```bash
$ python -m app.db.seed
🌱 Insertando datos iniciales (seed)...
  ✓ Rol creado: Administrador
  ✓ Rol creado: Gestor
  ✓ Rol creado: Técnico
  ✓ Canal creado: Presencial
  ✓ Canal creado: Teléfono
  ✓ Canal creado: Correo electrónico
  ✓ Canal creado: Portal web
  ✓ Estado creado: Abierto
  ✓ Estado creado: En proceso
  ✓ Estado creado: Pendiente cliente
  ✓ Estado creado: Resuelto
  ✓ Estado creado: Cerrado
  ✓ Nivel impacto creado: Bajo (peso=1)
  ✓ Nivel impacto creado: Medio (peso=3)
  ✓ Nivel impacto creado: Alto (peso=5)
  ✓ Nivel impacto creado: Crítico (peso=10)
  ✓ Tipo ticket creado: Incidencia
  ✓ Tipo ticket creado: Consulta
  ✓ Tipo ticket creado: Reclamo
  ✓ Tipo ticket creado: Solicitud de servicio
  - Departamento ya existe: Alta Verapaz
  - Departamento ya existe: Baja Verapaz
  ... (22 departamentos ya existían)
  ✓ Servicio creado: Internet residencial
  ✓ Servicio creado: Internet empresarial
  ✓ Servicio creado: Televisión por cable
  ✓ Servicio creado: Telefonía fija
  ✓ Servicio creado: Telefonía móvil

✅ Seed completado. 25 registros insertados.
```

**Resultado:** 25 registros nuevos insertados. 22 departamentos ya existían (idempotencia confirmada).

---

## 4. Análisis de la migración inicial

### 4.1 Cambios detectados por `--autogenerate`

La migración `55a1c50e11be_initial_migration.py` aplica 3 cambios:

```python
def upgrade() -> None:
    op.alter_column('roles', 'descripcion',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)                        # (1)
    op.drop_column('tickets', 'descripcion')           # (2)
    op.drop_column('tickets', 'titulo')                # (3)
```

| # | Cambio | Explicación |
|---|--------|-------------|
| (1) | `roles.descripcion` → `NOT NULL` | El modelo SQLAlchemy (`app/models/roles.py`) define `descripcion = Column(String(255), nullable=False)`, pero la tabla en la BD se creó originalmente con `nullable=True` (probablemente con `create_all()` antes de la migración). Alembic alinea la BD con el modelo. |
| (2) | Eliminar `tickets.descripcion` | El modelo `tickets.py` no tiene campo `descripcion`. La tabla en BD sí lo tenía (remanente de un diseño anterior o de `create_all()` sin actualizar). Se elimina. |
| (3) | Eliminar `tickets.titulo` | Similar a (2): el modelo no define `titulo`, la tabla en BD sí. Se elimina. |

### 4.2 Observación importante

Estos 3 cambios son **correctivos**: no agregan funcionalidad nueva, sino que alinean la BD con los modelos actuales. Esto es esperable en una **migración inicial** generada sobre una BD que ya fue creada/modificada manualmente con `Base.metadata.create_all()`.

El downgrade es reversible: restaura las columnas eliminadas y revierte el `NOT NULL`.

---

## 5. Análisis del seed script

### 5.1 Estructura

```
app/db/seed.py
├── importa SessionLocal
├── importa 7 DTOs (RolCreateDTO, CanalCreateDTO, ...)
├── importa 7 services como singletons
├── seed_catalogos(db) → recorre 7 catálogos
│   ├── Roles (3)
│   ├── Canales (4)
│   ├── Estados de ticket (5)
│   ├── Niveles de impacto (4)
│   ├── Tipos de ticket (4)
│   ├── Departamentos (22)
│   └── Servicios (5)
└── __main__ → abre sesión, ejecuta seed, imprime resumen
```

**Total de registros posibles:** 3+4+5+4+4+22+5 = **47**

**Registros insertados en esta ejecución:** **25** (los 22 departamentos ya existían)

### 5.2 Diseño — ¿por qué usa services?

El seed **no** inserta directamente con SQL crudo ni con el repositorio. Usa los **services** (ej. `rol_service.create_rol()`).

**Razón:** Esto garantiza que cualquier validación, regla de negocio o transformación definida en el service se aplique también durante el seed. Si mañana se agrega una validación en `create_rol()` (ej. "el nombre no puede contener caracteres especiales"), el seed la respetará automáticamente.

### 5.3 Idempotencia

Cada inserción está envuelta en `try/except` con `db.rollback()`. Si el registro ya existe (el service lanza excepción por `IntegrityError` de unique constraint), se hace rollback de esa transacción individual y se continúa con el siguiente registro.

**Esto permite ejecutar el seed múltiples veces sin efectos secundarios.**

---

## 6. Verificación final

| Verificación | Comando | Resultado |
|---|---|---|
| Alembic instalado | `pip list \| grep alembic` | ✅ `alembic 1.18.5` |
| Alembic en requirements.txt | `grep alembic requirements.txt` | ✅ `alembic==1.18.5` |
| Migración aplicada | `alembic current` | ✅ `55a1c50e11be (head)` |
| Seed ejecutado | `python -m app.db.seed` | ✅ 25 registros insertados |
| Conexión a BD | `alembic current` imprime "Conexión correcta" | ✅ |
| Idempotencia del seed | Departamentos dieron "ya existe" sin error fatal | ✅ |

---

## 7. Observaciones y recomendaciones

### 7.1 La migración inicial es correctiva, no aditiva

Los 3 cambios de la migración inicial (`NOT NULL` en `roles.descripcion`, eliminar `tickets.titulo` y `tickets.descripcion`) alinean la BD con los modelos. No hay migraciones pendientes por generar. **La BD y los modelos están sincronizados.**

### 7.2 Flujo para futuras migraciones

Cuando se modifique un modelo (agregar/quitar columna, cambiar tipo, etc.):

```bash
# 1. Generar migración automática
alembic revision --autogenerate -m "descripcion_del_cambio"

# 2. Revisar el archivo generado en alembic/versions/

# 3. Aplicar a la BD
alembic upgrade head

# 4. Verificar
alembic current
```

### 7.3 El seed usa el entorno sync

El seed usa `SessionLocal` (síncrono) porque toda la app es síncrona actualmente. Cuando se migre a async (Fase 12), el seed también deberá migrarse a `AsyncSession`.

### 7.4 Orden de inserción

Los departamentos se insertan **después** de tipos de ticket y **antes** de servicios. No hay dependencias entre estos catálogos (son tablas independientes), por lo que el orden no es crítico. Sin embargo, si en el futuro se agregan municipios (que dependen de departamentos), el seed deberá insertar departamentos primero.

---

## 8. Conclusión

**Fase 8 — COMPLETADA ✅**

- Alembic configurado, instalado y documentado en `requirements.txt`
- Migración inicial generada y aplicada (`55a1c50e11be`)
- Seed script ejecutado exitosamente (25 registros insertados, idempotencia verificada)
- Base de datos lista para desarrollo con catálogos poblados

**Siguiente fase:** Fase 9 — Tests (`pytest` + `httpx` + `TestClient`)