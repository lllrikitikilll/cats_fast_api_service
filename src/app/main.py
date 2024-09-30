from fastapi import FastAPI

from src.app.api.cat_handlers import router

app = FastAPI()
app.include_router(router)
