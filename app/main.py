from fastapi import FastAPI

from app.api.routers.ticket_router import router as ticket_router


app = FastAPI(title="project_final")
fastapi_app = app

app.include_router(ticket_router)


@app.get("/")
def read_root():
    return {"message": "API project_final funcionando"}