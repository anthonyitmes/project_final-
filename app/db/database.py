from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# La URL de conexión sale de config.py para no dejar credenciales fijas en el código.
DATABASE_URL = settings.DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    # Esta función se usa como dependencia de FastAPI para abrir y cerrar la sesión.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
