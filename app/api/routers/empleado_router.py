from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.empleado_dto import (
    EmpleadoCreateDTO,
    EmpleadoResponseDTO,
    EmpleadoUpdateDTO,
)
from app.services.empleado_service import empleado_service

empleado_services = empleado_service()
router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post(
    "", 
    response_model=EmpleadoResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un empleado",
    description="Crea un nuevo empleado en el sistema."
)
def create_empleado(
    empleado_in: EmpleadoCreateDTO,
    db: Session = Depends(get_db)
) -> EmpleadoResponseDTO:
    """Crea un nuevo empleado en el sistema.

    - **nombre**: nombre del empleado.
    - **apellido**: apellido del empleado.
    - **email**: correo electrónico del empleado.
    - **telefono**: número de teléfono del empleado.
    """
    return empleado_services.create_empleado(db, empleado_in)

@router.get(
    "",
    response_model=list[EmpleadoResponseDTO],
    summary="Listar todos los empleados",
    description="Obtiene la lista completa de empleados registrados en el sistema."
)
def get_all_empleados(
    db: Session = Depends(get_db)
) -> list[EmpleadoResponseDTO]:
    """Obtiene la lista completa de empleados registrados en el sistema."""
    return empleado_services.get_all_empleados(db)

@router.get(
    "/{id_empleado}",
    response_model=EmpleadoResponseDTO,
    summary="Obtener un empleado por ID",
    description="Obtiene un empleado específico por su ID."
)
def get_empleado_by_id(
    id_empleado: int,
    db: Session = Depends(get_db)
) -> EmpleadoResponseDTO:
    """Obtiene un empleado específico por su ID.

    - **id_empleado**: ID del empleado a buscar.
    """
    return empleado_services.get_empleado_by_id(db, id_empleado)

@router.patch(
    "/{id_empleado}",
    response_model=EmpleadoResponseDTO,
    summary="Actualizar un empleado por ID",
    description="Actualiza la información de un empleado específico por su ID."
)
def update_empleado(
    id_empleado: int,
    empleado_update: EmpleadoUpdateDTO,
    db: Session = Depends(get_db)
) -> EmpleadoResponseDTO:
    """Actualiza la información de un empleado específico por su ID.

    - **id_empleado**: ID del empleado a actualizar.
    - **empleado_update**: Datos actualizados del empleado.
    """
    return empleado_services.update_empleado(db, id_empleado, empleado_update)

@router.delete(
    "/{id_empleado}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un empleado por ID",
    description="Elimina un empleado específico por su ID."
)
def delete_empleado(
    id_empleado: int,
    db: Session = Depends(get_db)
) -> None:
    eliminado = empleado_services.delete_empleado(db, id_empleado)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {id_empleado} no encontrado",
        )
    
