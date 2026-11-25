import uvicorn
from fastapi import FastAPI
from app.controllers.upload_controller import router as upload_router
from app.controllers.query_controller import router as query_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(query_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)