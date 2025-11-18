from fastapi import FastAPI
from app.database import Base, engine
from app.api import router as api_router # Importa o router que uniu tudo

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Move+ API B2B is running! Go to /docs for testing."}