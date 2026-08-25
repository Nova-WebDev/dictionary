from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.data.init_db import init_db
from app.redis.redis_client import redis_client
from app.errors import DomainError
from app.utils.logger import logger

from routers.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.dictionary_router import router as dictionary_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield
    await redis_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error(str(exc), exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(dictionary_router, prefix="/words", tags=["dictionary"])