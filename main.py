"""
Запуск сервера - uvicorn main:app --host localhost --port 8000 --reload

Пошук по імені -  http://127.0.0.1:8000/api/contacts/?first_name=
Пошук по прізвищу -  http://127.0.0.1:8000/api/contacts/?last_name=
Пошук по email -  http://127.0.0.1:8000/api/contacts/?email=

Список контактів з днями народження на найближчі 7 днів - http://127.0.0.1:8000/api/contacts/?birthdays=7
Можна знайти список контактів на будь-яку кількість днів - змінити 7 на потрібну кількість днів
"""

import redis.asyncio as redis_asyncio

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users
from src.conf.config import settings

import uvicorn

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis_asyncio.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                                  decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "FastAPI Contacts"}


@app.get("/api/healthchecker")
def root():
    return {"message": "Is working."}


origins = ["http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
