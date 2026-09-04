FROM dictionary-base

WORKDIR /app

COPY . .

CMD ["sh", "-c", "alembic upgrade head && gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:8000"]
