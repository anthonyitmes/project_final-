from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# La URL de conexión sale de config.py para no dejar credenciales fijas en el código.
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    url=DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Conexión correcta a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

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
