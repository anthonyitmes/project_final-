from fastapi import FastAPI
print("Hello, World!")

fastapi_app = FastAPI()
@fastapi_app.get("/")
def read_root():
    return {"Hello": "World"}ls