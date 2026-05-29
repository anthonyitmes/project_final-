# app/models/__init__.py

from app.db import Base

from .canales import Canal
from .clientes import Cliente
from .clientes_servicios import ClienteServicio
from .departamentos import Departamento
from .direcciones import Direccion
from .empleados import Empleado
from .estado_ticket import EstadoTicket
from .municipios import Municipio
from .niveles_impacto import NivelImpacto
from .plantilla_formulario import PlantillaFormulario
from .roles import Rol
from .servicios import Servicio
from .tickets import Ticket
from .tipos_ticket import TipoTicket
