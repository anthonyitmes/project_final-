"""
Schemas comunes reutilizables en toda la API.

- PaginatedResponse[T]: respuesta genérica paginada para endpoints de listado.
  Usa Generic[T] de Pydantic para que Swagger muestre el tipo concreto (ej: PaginatedResponse[ClienteResponseDTO]).
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica.

    Se usa como response_model en endpoints GET de listado:
        @router.get("", response_model=PaginatedResponse[ClienteResponseDTO])
        def get_all_clientes(page: int = 1, size: int = 20, ...) -> PaginatedResponse:
            ...

    Campos:
        items: listado de registros de la página actual.
        total: cantidad total de registros en la base de datos.
        page:  número de página actual (1-based).
        size:  cantidad máxima de registros por página.
        pages: cantidad total de páginas (ceil(total / size)).
    """

    items: list[T]
    total: int
    page: int
    size: int
    pages: int