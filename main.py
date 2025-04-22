# from fastapi import FastAPI

# from contextlib import asynccontextmanager
#
# from database import create_tables, delete_tables
# from router import router as tasks_router



# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_tables()
#     print("База очищена")
#     await create_tables()
#     print("База готова к работе")
#     yield
#     print("Выключение")


# app = FastAPI(lifespan=lifespan)
# app.include_router(tasks_router)


# @app.get(path="/", tags=["Главная"])
# async def root():
#     return {"message": "Hello from FastAPI!"}




from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.routes import router as api_router


app = FastAPI(title="Simple Analysis and Forecasting TimeSeries")
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки. В продакшене укажите конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
