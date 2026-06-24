from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # Valores con defaults (si no están en el .env, usa estos)
    PROJECT_NAME: str = "project_final"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Credenciales de Base de Datos (Nota que DB_PORT es int)
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "12345678"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "user_db"

    # Seguridad (Al no tener default, Pydantic exigirá que JWT_SECRET_KEY exista sí o sí en el .env)
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración: Le dice a Pydantic que lea automáticamente el archivo .env
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """Propiedad computada que ensambla la URL automáticamente"""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Instancia de importación
settings = Settings()