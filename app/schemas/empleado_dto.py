from pydantic import BaseModel, EmailStr

class EmpleadoCreateDTO(BaseModel):
    nombre_empleado: str
    email: EmailStr
    password_bash: str
    activo: bool
    id_rol: int

class EmpleadoResponseDTO(BaseModel):
    id_empleado: int
    nombre_empleado: str
    email: EmailStr
    activo: bool
    id_rol: int

    model_config = {
        "from_attributes": True
    }

class EmpleadoUpdateDTO(BaseModel):
    nombre_empleado: str | None = None
    email: EmailStr | None = None
    password_bash: str | None = None
    activo: bool | None = None
    id_rol: int | None = None
