from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import DomainError
from app.utils.logger import logger
from routers.auth_router import router as auth_router

app = FastAPI()


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error(str(exc), exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})


app.include_router(auth_router)
