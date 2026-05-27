# app/models/__init__.py

# 1. Primero importas la Base (necesaria para Alembic)
from app.db import Base

# 2. Luego importas todas tus tablas
from .tickets import Ticket
from .empleados import Empleado
from .clientes import Cliente