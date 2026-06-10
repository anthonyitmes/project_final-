import os

from dotenv import load_dotenv


# Si existe un archivo .env en la raíz del proyecto, se cargan sus variables.
load_dotenv()


class Settings:
    """Configuración central de la aplicación.

    La idea de este archivo es concentrar aquí los valores que cambian entre
    entornos: desarrollo, pruebas y producción.

    En vez de escribir credenciales directamente en el código, leemos variables
    de entorno. Eso evita exponer contraseñas en el repositorio y permite usar
    la misma base de código en distintos servidores.
    """

    def __init__(self) -> None:
        # Nombre visible de la aplicación.
        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "project_final")

        # Ruta base de la API si luego quieres versionarla, por ejemplo /api/v1.
        self.API_V1_STR = os.getenv("API_V1_STR", "/api/v1")

        # DEBUG controla si SQLAlchemy imprime consultas y si la app corre en modo desarrollo.
        self.DEBUG = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}

        # Credenciales y datos de conexión por separado.
        # Esto es útil cuando tu hosting te da usuario, contraseña, host y puerto por separado.
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "User")

        # Configuracion JWT.
        # JWT = JSON Web Token: se usa para autenticar usuarios sin guardar la sesion en el servidor.
        # El secreto debe venir del entorno y no debe quedar hardcodeado en el repositorio.
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

        # Si se define DATABASE_URL, se usa completa. Si no existe, se arma con las piezas.
        self.DATABASE_URL = os.getenv("DATABASE_URL") or self._build_database_url()

    def _build_database_url(self) -> str:
        # Se arma una URL compatible con SQLAlchemy y PostgreSQL.
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instancia única para importar desde cualquier parte del proyecto.
settings = Settings()
